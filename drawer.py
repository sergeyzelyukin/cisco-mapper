#!/usr/bin/env python

import yaml
import json
import sys
import os
from ciscomapper import print_cisco_network, change_root


if __name__ == "__main__":	
  """Sample tool for drawing the network hierarchy, modify for yourself
  """
  if len(sys.argv)>=2:
    network_map_filename = sys.argv[1]
    if len(sys.argv)>=3:
      new_root = sys.argv[2]
    else:
      new_root = None
  else:
    print "usage: %s network_map.json [new_root_board_id]"%(sys.argv[0])
    sys.exit(1)

  if not os.path.exists(network_map_filename):
    print "file '%s' not found"%(network_map_filename)
    sys.exit(1)

  with open(network_map_filename, "r") as fh:
    devices_map = json.load(fh)
    
  if new_root:
    if new_root in devices_map.keys():
      change_root(devices_map, new_root)

  print_cisco_network(devices_map, show_ip=True, show_board_id=True)

