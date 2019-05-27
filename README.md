# cisco-mapper
Draw the scheme of your cisco network, all you need is telnet access and cdp enabled.

IMPORTANT: Before running this, please make sure that CDP is disabled on all untrusted ports. If someone pretends as a CDP neighbor, he/she can steal all your passwords! Use this approach at your own risk!

First of all, please, install "ciscotelnet" module:
<pre>
pip install git+https://github.com/sergeyzelyukin/cisco-telnet.git
</pre>
Now you can use this module.

Calling the: 
<pre>
browse_cisco_network(start_ip, dictionary1, [], auth_tokens)
</pre>
function, you will finally have a dictionary like:

<pre>
dictionary1["CAT111222"]["hostname"]	= "R1"
dictionary1["CAT111222"]["ip"]		= "192.168.10.99"
dictionary1["CAT111222"]["depths"]	= "3"
dictionary1["CAT111222"]["children"]	= ["CHK333555", "FD0777888"]
...
dictionary1["CHK333555"]["hostname"]	= "C5"
...
dictionary1["FD0777888"]["hostname"]	= "R99"
...
</pre>

Just calling the:
<pre>
for board_id in dictionary1.keys():
	print dictionary1[board_id]["hostname"]
	print dictionary1[board_id]["ip"]
</pre>
you will have all cisco devices in you network.

You can save this dictionary to yaml or json file and next time preload it, instead of new browsing.

Having this dictionary, you can call: 
<pre>
print_cisco_network(dictionary1) 
</pre>
and draw scheme like this:
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
</pre>

If you want to look at the network from other point of view, you can recompile the hierarchy and print it again:
<pre>
change_root(dictionary1, "CAT01234567")
print_cisco_network(dictionary1, show_ip=False) 
</pre>

You should specify the board_id value of new root device to uniquely identify it. The board_id can be found directly in the dictionary (it is a key) or can be printed with:
<pre>
print_cisco_network(dictionary1, show_board_id=True)
</pre>

By default browse_cisco_network() function uses "depths first" algorithm it is useful for drawing instant (while crawling) schemes, but it can lead to wrong schemes in ring topologies.
There is also "breadth first" algorithm, which creates schemes much closer to reality, but it cannot draw hierarchy during network crawling.
Both methods could be called directly:
<pre>
browse_cisco_network_depth1st(start_ip, dictionary1, [], auth_tokens) # "depth first" algorithm
# or
browse_cisco_network_breadth1st(start_ip, dictionary1, [], auth_tokens) # "breadth first" algorithm
</pre>

Full params list:
browse_cisco_network(start_ip, devices_map, skip_neighbors, auth_tokens, max_deep, verbose, call_for_every_device)

Please find examples in sample.py.

