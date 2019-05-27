#!/usr/bin/env python

import ciscotelnet
import yaml
import json
import sys
from ciscomapper import browse_cisco_network_breadth1st, print_cisco_network, browse_cisco_network_depth1st, browse_cisco_network


if __name__ == "__main__":
  """Sample tool for network crawling, modify for yourself
  """
  ciscotelnet.WAIT_TIMEOUT = 60 # IMPORTANT, module requirement

  if len(sys.argv)>=3:
    auth_choices_filename = sys.argv[1]
    start_hostname = sys.argv[2]
  else:
    print "usage: %s auth_choices.yaml start_hostname"%(sys.argv[0])
    sys.exit(1)

  with open(auth_choices_filename, "r") as fh: 
    auth_choices = yaml.load(fh)

  devices_map = {} 
  try:
    browse_cisco_network_depth1st(start_hostname, devices_map, [], auth_choices)
    #browse_cisco_network_breadth1st(start_hostname, devices_map, [], auth_choices)
  except Exception as msg:
    print "unable to browse network, msg='%s'"%(msg)
    sys.exit()

  """
  with open("network_map.yaml", "w") as fh:
    yaml.dump(devices_map, fh, default_flow_style=False)
  """

  with open("network_map.json", "w") as fh:
    json.dump(devices_map, fh, separators=(",", ": "), indent=2)

