#!/usr/bin/env python

import ciscotelnet
import yaml
import json
import sys
from ciscomapper import browse_cisco_network, print_cisco_network


def do_something_with_device_while_crawling(hostname, ip, auth_token):
  """ This function will be called for each device, while mapping process is active.
  You can do something with every found device (backup?)
  """
  print hostname
  print ip
  #print auth_token
  print "-"*10


if __name__ == "__main__":
  ciscotelnet.WAIT_TIMEOUT = 60 # IMPORTANT, module requirement

  """ 
  variour devices could have different login credentials,
  specify all possible auth tokens here:
  auth_choices = [
    {"final_mode":ciscotelnet.MODE_ENABLE, "user":"mary", "user_pass":"12345", "enable_pass":"none", "line_pass":"none"},
    {"final_mode":ciscotelnet.MODE_EXEC, "user":"peter", "user_pass":"qwerty", "enable_pass":"none", "line_pass":"none"},
    {"final_mode":ciscotelnet.MODE_EXEC, "user":"none", "user_pass":"none", "enable_pass":"none", "line_pass":"777777"},
    ]
  """

  # or load auth tokens from yaml file, saved before with yaml.dump()
  with open("auth_choices.conf", "r") as fh: 
    auth_choices = yaml.load(fh)

  # run sometimes to be updated with network scheme 
  devices_map = {} # when browse_cisco_network() ends, this dictionary will be filled with the cisco devices and their hierarchy
  try:
    browse_cisco_network("10.100.1.9", devices_map, [], auth_choices) # will start browsing, with no limits in depts, and will print scheme while discovering new devices
    # or
    browse_cisco_network("10.100.1.9", devices_map, [], auth_choices, max_deep=1) # limit the depts
    # or
    browse_cisco_network("10.100.1.9", devices_map, [], auth_choices, max_deep=3, verbose=False) # and do not print anything
    # or
    browse_cisco_network("10.100.1.9", devices_map, [], auth_choices, max_deep=1, verbose=False, call_for_every_device=do_something_with_device_while_crawling) # and treat each found device before mapping ends
  except Exception as msg:
    print "unable to browse network, msg='%s'"%(msg)
    sys.exit()

  # save map to yaml for future use
  with open("cisco_network_map.yaml.txt", "w") as fh:
    yaml.dump(devices_map, fh, default_flow_style=False)

  # or save map to json
  with open("cisco_network_map.json.txt", "w") as fh:
    json.dump(devices_map, fh, separators=(",", ": "), indent=2)


  # any time load map from yaml ot json
  with open("cisco_network_map.json.txt", "r") as fh:
    devices_map = json.load(fh)

  # and draw it
  print_cisco_network(devices_map) # print text scheme hierarchically
  

