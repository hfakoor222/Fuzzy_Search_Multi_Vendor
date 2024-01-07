

Program searches routers and switches for fuzzy matches: cisco, junos routers/switches and ASA firewalls.
User inputs  +   and   (())   control characters in a notepad file, along with bare bones configuration templates. 


•	+ is equal to search anything non-greedy,  and includes spaces

•	(())  is equal to any characters no spaces. This gives the user absolute control in template definition. (i.e. 10.0.1.(()) matches any 10.0.1.x subnet) .

•	#   The hashtag sign means any character, and 1 line, or more than 1 line. It can read the whole device configuration.  

Multiple search patterns can be categorized for certain ip_addresses and fed into the script at once.
Script can validate a misconfigured subnet by 1 binary digit, musconfigured acl, etc

Example 1:

    router bgp **_+_**                                
    neighbor 10.1._**(())**_                                                                                                                                  
    neighbor _**(())**_ remote-as 65002


This configuration finds any bgp protocols on the device, that include a neighbor in the subnet **10.1.x.x**  and that
also have a neighboring AS of 65002. We can validate bgp configurations.

Example 2:

ip access-list +  
deny udp + range 1025-(()) 

This finds any Cisco device in your network that does or doesn't  have any UDP deny statement involved. If your policy is to deny port ranged 1025-65534 ranges, we can find devices that do or don't have this policy enabled.


Example 3:

 	router bgp (())
 	+
 	address-family ipv6 +

finds all IPv6 globally enabled bgp devices. If for example we find out our IPv6 is propgating correctly, we can find out where bgp isn't configured for IPv6.





has been tested on Cisco routers, switches, and ASAv. I will be uploading code for Junos scraping soon, and also a video of the code working against ASA (tested last night).




Refer to "config_documentation.txt"   for instructions and the template+config.py file  for the code.







https://github.com/hfakoor222/Fuzzy_Search_Multi_Vendor/assets/105625129/2b42e85b-e1a5-4c18-a255-4f664b00de68







I will be uploading a AWS API and parser to this soon

:face_exhaling:



