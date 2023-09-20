Program searches routers and switches for fuzzy matches.
User inputs  +   and   (())   control characters in a notepad file, along with bare bones configuration templates, the program does fuzzy searching. 


•	+ is equal to search anything non-greedy,  and includes spaces



•	(())  is equal to any characters no spaces. This gives the user absolute control in template definition.

•	#   The hashtag sign means any character, and 1 line, or more than 1 line. It can read the whole file.

Example:

 router bgp **_+_**                                
 neighbor 10.1._**(())**_                                                                                                                                  
 neighbor _**(())**_ remote-as 65002


This configuration finds any bgp protocols on the device, that include a neighbor in the subnet **10.1.x.x**  and that
also have a neighboring AS of 65002

Example 2:

 router bgp **(())**
 +
 network 2001:db8:**(())**

finds all IPv6 globallly enabled bgp devices.

has been tested on Cisco routers, switches, and ASAv. I will be uploading code for Junos scraping soon, and also a video of the code working against ASA (tested last night).


refer to "config_documentation.txt"   for instructions

and the template+config.py file  for the code







https://github.com/hfakoor222/Fuzzy_Search_Multi_Vendor/assets/105625129/2b42e85b-e1a5-4c18-a255-4f664b00de68








![alt text](https://media.giphy.com/media/20JY76TfKAhR20SfJu/giphy.gif)



