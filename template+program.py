
import re
import netmiko
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
import time


junos_command = "show configuration"
ios_command = "show running-config"
asa_command = "show running-config"

outfile = open("outfile.txt", "a+")

with open("device_template.txt", "r") as dev_template:
    dev_template = dev_template.read()

dev_list = dev_template.split("$$$")
dev_list = dev_template.split("$$$")
global configuration_blocks
for i in dev_list:

    configuration_blocks = i.split("$$")
    # we get our configuration text to perform fuzzy searches later
    configuration_blocks = configuration_blocks[1:]
    #we remove the ip addres list header
    #configuration_blocks.strip()
    # we delete the last item in list if empty, incase user leaves blank lines
    configuration_blocks = [sub.replace("\n", "",1) for sub in configuration_blocks]
    #replacing first occurence of \n in the split
    configuration_blocks = [sub.replace("$", ".*?").replace("(())", r"\S+" ) for sub in configuration_blocks]
    #this is where we pass in fuzzy search characters for regex parsing
    # notice we made this a non-greedy quantifier with  .*?  so the user can input  $ in the file as a substitute for an any text line
    template = re.search("\w+_template$", i, re.MULTILINE)
    # we use this for device type/template later: multiline option used for surety in case someone mistypes
    template = template.group()
    #save string result to a variable to use later
    address_list = re.search("ip_address.*]]", i, re.DOTALL)
    # here we get our netmiko conenction parameters
    updated_address = re.search("\[\[.*]]", address_list.group(), re.DOTALL )
    # we need to use DOTALL to make '.*' match newline '\n', and so the user can format the textfile string on many or 1 line
    #this is so the user can type ip_address list in any format
    updated_address = updated_address.group().replace("]]", "]")
    updated_address= re.sub(r'[\x00-\x1f]', '', updated_address)
    #here we remove control characters in textpad user may have put in when they type: removes tabs, spaces, blank lines
    updated_address=  updated_address.split("],")
    updated_address = [sub.replace("[[","").replace("]", "").replace("[", "") for sub in updated_address]
    #we now have a formatted list
    if template == "ios_template":  ios_address_list, ios_template = updated_address, template
    if template == "junos_template": junos_address_list, junos_template = updated_address, template
    if template == "asa_template": asa_address_list, asa_template,  = updated_address, template

    #we now have all the variables we need to do fuzzy searching against devices, they are split into lists and easy to use

    # I will define a function below and use it many times, good for threading
    def connection_handler( address_list,  dev_type = "autodetect"):
            print(configuration_blocks)
            for i in address_list:
                var = i.split(",")
                ip_address, username, password, secret = str(var[0]).strip(),\
                    str(var[1]).strip(), str(var[2]).strip(), str(var[3]).strip()

                dev_type= 'cisco_ios'
                print("*" * 8)
                # print( configuration_blocks)

                connection = ConnectHandler(host=str(ip_address), username=username, password=password,
                                                              secret=secret, device_type=dev_type)

                connection.enable()
                result = connection.send_command("show run")
                result = result.replace("\n ", "\n")
                #print(result)
                for i in configuration_blocks:
                    res = re.search(i, result,re.DOTALL)
                    if res: print("found match")
                    if res: print(res.group() + "\n")
                    if res:
                        outfile.write("Found match for:  " + template + " " +  ip_address + "\n" + "*" * 20 + "\n")

                        outfile.write(res.group() + "\n")
                    if not res:
                        outfile.write("Config not found for   " + template + " " + ip_address + "\n" + "*" *20 + "\n")
                        outfile.write(i + "\n")


    connection_handler(ios_address_list, "cisco_ios")

    #connection_handler(junos_address_list, "juniper_junos")
    #connection_handler(asa_address_list, "cisco_asa")

    #connection_handler( vendor_address_list, "autodetect")








