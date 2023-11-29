Program searches routers and switches for fuzzy matches: cisco, junos routers/switches and ASA firewalls.
User inputs  +   and   (())   control characters in a notepad file, along with bare bones configuration templates. We can feed multiple search patterns to hundreds of devices, search patterns and ip addresses can be categorized; all of this is fed in one form feed .txt file.


•	+ is equal to search anything non-greedy,  and includes spaces



•	(())  is equal to any characters no spaces. This gives the user absolute control in template definition.

•	#   The hashtag sign means any character, and 1 line, or more than 1 line. It can read the whole device configuration.
Example:

  router bgp **_+_**                                
  neighbor 10.1._**(())**_                                                                                                                                  
  neighbor _**(())**_ remote-as 65002


This configuration finds any bgp protocols on the device, that include a neighbor in the subnet **10.1.x.x**  and that
also have a neighboring AS of 65002

Example 2:

 	router bgp (())
 	+
 	network 2001:db8:(())

finds all IPv6 globally enabled bgp devices. If for example we find out our IPv6 routing is slow, we can find out where bgp isn't configured for IPv6.

has been tested on Cisco routers, switches, and ASAv. I will be uploading code for Junos scraping soon, and also a video of the code working against ASA (tested last night).


The advantage to this script is mutlivendor, supporting up to 90% of existing vendors with the underlying library, and that it runs quicker than standard network monitoring tools (it is threaded), and gives us customized code control.

Refer to "config_documentation.txt"   for instructions and the template+config.py file  for the code.







https://github.com/hfakoor222/Fuzzy_Search_Multi_Vendor/assets/105625129/2b42e85b-e1a5-4c18-a255-4f664b00de68








:face_exhaling:



