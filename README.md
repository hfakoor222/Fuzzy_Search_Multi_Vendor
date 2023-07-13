# Fuzzy_Search_Multi_Vendor


#######################################################################################################
Welcome to configuration template parser program. This program parses multivendor devices.
Currently ASA, Cisco IOS, IOS-XE,  and Juniper router devices are supported.
We input a template and compare fuzzy searches across devices and return matches if exists.

the port in your environment should be set to 22 for SSH
make sure to allow python through your firewall

program splits device templates using  $$$  and splits configurations fed into each template/device using   $$

to add a configuration template begin with a configuration template name:
supported names:
asa_template
ios_template
junos_template


after which we add a list of lists (enclosed in exterior brackets) for ip addresses and connection information

ip_address = [[ip_address1 , username1 , password1, SSH_password1 ], [ip_address2, username2, password2, ""]] 

notice the double brackets at the beginning and end.  The SSH password can be an empty string if desired, depending on device platform.
junos does not require a secret for running this script, we leave blank by using "" or can use root user pass

example:
ip_address = [[10.0.0.1, cisco, cisco123, secret], [10.0.0.2, cisco, cisco123, secret],
		[10.0.0.3, user_x, password_x, secret]
		[10.0.0.4, user_x, password_x, secret]]


after this we can define our templates. 

Templates are parsed using $, and (())
$ signifies any characters (ascii), spaces, and a optional newline,
whereas (()) signifies any characters without spaces,  
in regular-expression terms:
$     =  .*[\n]?
(())  =  \S+
(()) signifies at least 1 character must exist.
 
so for example:

router ospf ((5))
router-id $
network $ area 0

means that this configuration below

router ospf 6
router-id 5.5.5.5
domain-tag 55
network 192.168.0.0 0.0.0.255 area 0

will be found due optional match (())
and  $ =  any character (in this case 5.5.5.5)

we can also do this:

router ospf $
$
network 192.168.0.0

and it will match. We do not need to include $ as an "any characters in this line"
as the searches find similar string patterns in the device configuration, after the configuration templates is split.


for example in a cisco "show run" we see:
!
interface Serial1/3
 no ip address
!
router eigrp 65001
 network 10.0.0.0
 network 192.168.14.0
!
router bgp 65001
 bgp log-neighbor-changes
 network 10.1.1.0 mask 255.255.255.0
 neighbor 10.1.103.3 remote-as 65001
 neighbor 10.2.2.2 remote-as 65001
 neighbor 10.2.2.2 update-source Loopback1
 neighbor 192.168.14.5 remote-as 65002
!


and we split the configuration via  "!"  symbol

so we will be matching on the below for example:

interface Serial1/3
 no ip address

and also on

router bgp 65001
 bgp log-neighbor-changes
 network 10.1.1.0 mask 255.255.255.0
 neighbor 10.1.103.3 remote-as 65001
 neighbor 10.2.2.2 remote-as 65001
 neighbor 10.2.2.2 update-source Loopback1
 neighbor 192.168.14.5 remote-as 65002

We can include both fuzzy and exact templates under the same configuration template for deeper searches.

example:

ios_template
ip_address = [[10.0.0.1, cisco, cisco123, secret], [10.0.0.2, cisco, cisco123, secret1],
		[10.0.0.3, user_x, password_x, secret2]
		[10.0.0.4, user_x, password_x, secret3]]
router bgp 65001
neighbor 10.1.$
neighbor 10.1.103.3 remote-as 65002
$$
router bgp $
neighbor 10.1.1.0
neighbor $ remote-as 65002
$$
router bgp $
neighbor $
neighbor $ remote-as $


will return the above bgp result. However the first will return an exact match of 'router bgp 65001',
the second will return router bgp (any as), with a neighbor 10.1.1.0,
and the third will return any router bgp (as)  with any neighbor any ip address and any remote-as.






here is a full example:


ios_template
ip_address = [[10.0.0.1, cisco, cisco123, secret], [10.0.0.2, cisco, cisco123, secret],
		[10.0.0.3, user_x, password_x, secret]
		[10.0.0.4, user_x, password_x, secret]]
router bgp 65001
neighbor 10.1.$
neighbor 10.1.103.3 remote-as 65002
$$
router bgp $
neighbor 10.1.(()).(())
neighbor $ remote-as 65002
$$
router ospf (())
router-id (())
network 10.1.(()).(()) area (())
$$$
junos_template
ip_address = [[10.5.5.5, junos, junos123, ""], [10.6.6.6, junos_user2, junos1234, ""],
			[10.7.7.7, junos_user2, junos12345,""]]






please note although these are fuzzy searches and will do "loose" searches,
the order of the configuration matters

i.e:
router ospf 3
network $
router-id 1.1.1.1

will not match the cisco device configs

but
router ospf 3
router-id 1.1.1.1
network $


matches the device configuration as it is in the same running order found on the device

in this case we can use $ as "any characters in this line" for more granular control

for example:

router ospf 3
$
router-id 1.1.1.1
$
network $
$
$
