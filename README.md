# cisco-mapper
Draw the scheme of your cisco network, all you need is telnet access and cdp enabled

Calling "browse_cisco_network()" function, you will finally have a dictionary like:
<pre>
dictionary1["CAT111222"]["hostname"]	= "R1"
dictionary1["CAT111222"]["ip"]		= "192.168.10.99"
dictionary1["CAT111222"]["depths"]	= "3"
dictionary1["CAT111222"]["children"]	= ["CHK333555", "FD0777888"]
dictionary1["CHK333555"]["hostname"]	= "C5"
...
dictionary1["FD0777888"]["hostname"]	= "R99"
...
</pre>

Just calling the:
<pre>
for board_id in dictionary1.keys():
	print dictionary1[board_id]["hostname"],
	print dictionary1[board_id]["ip"]
</pre>
you will have all cisco devices in you network.

You can save this dictionary to yaml or json file and next time preload it, instead of new browsing.

Having this dictionary, you can call "print_cisco_network()" and draw scheme like this:
<pre>
C9 (10.10.9.254)
        C6 (10.20.0.6)
        C8 (10.20.0.8)
                C21 (10.200.1.21)
                R1 (10.12.3.61)
                R2 (192.168.5.1)
        C10 (10.12.3.153)
                R10 (10.17.0.166)
                R30 (10.18.2.193)
                C11 (10.0.49.11)
                        R12 (10.17.40.221)
                C13 (10.20.45.13)
                        R9 (10.12.5.37)
</pre>>
