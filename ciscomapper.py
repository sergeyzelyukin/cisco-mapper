#!/usr/bin/env python

import ciscotelnet
import re


def from_string(s):
  """Functions to convert IPv4 address to integer and vice-versa.
  Written by Christian Stigen Larsen, http://csl.sublevel3.org
  Placed in the public domain by the author, 2012-01-11 
  https://gist.github.com/cslarsen/1595135
  """
  return reduce(lambda a,b: a<<8 | b, map(int, s.split(".")))


def browse_cisco_network(host, devices_map, skip_neighbors, auth_tokens, deep=0, max_deep=0, verbose=True, indent="\t", call_for_every_device=None):
  """This function logs in to cisco device,
  gets its board id (to use it as an unique identifier for the device),
  gets its hostname (for human readability),
  gets its highest ip,
  and gets its cdp neighbors. 
  Then it calls itself for each neighbor,
  if call ends well, it adds the neighbor to the list of current cisco device children 
  """

  for token_index,auth_token in enumerate(auth_tokens): # shuffle auth tokens
    with ciscotelnet.CiscoTelnet(host, verbose=False) as cisco:
      if cisco.login(final_mode=auth_token["final_mode"], user=auth_token["user"], user_pass=auth_token["user_pass"], enable_pass=auth_token["enable_pass"], line_pass=auth_token["line_pass"]):
        new_auth_tokens = auth_tokens[:]
        new_auth_tokens = [new_auth_tokens.pop(token_index)] + new_auth_tokens # place the success token to the top of the list
            
        output = cisco.cmd("sh version | i board ID") # get board ID for unique identification of the device
        m = re.search("^\s*Processor\s+board\s+ID\s+(\S+)", output, re.IGNORECASE)
        if m:
          board_id = m.group(1)
        else:
          raise(Exception("unable to get board_id, got '%s'"%(output)))

        output = cisco.cmd("sh version | i uptime") # get actual hostname from "sh version"
        m = re.search("^\s*(\S+)\s+uptime", output, re.IGNORECASE)
        if m:
          hostname = m.group(1)
        else:
          raise(Exception("unable to get hostname, got '%s'"%(output)))

        output = cisco.cmd("sh ip int brief | ex down|unassi|nterface") # get all ip addresses on up/up interfaces
        ips = []
        for line in output.split("\n"):
          m = re.search(r"^\s*\S+\s+(\d+\.\d+\.\d+\.\d+)", line, re.IGNORECASE|re.MULTILINE)
          if m:
            ips.append(m.group(1))
        if ips:
          highest_ip = sorted(ips, key=from_string)[-1]
        else:
          raise(Exception("unable to get ip address, got '%s'"%(output)))

        if board_id not in devices_map.keys():  # if we meet this device for the 1st time
          if verbose:
            print indent*deep+hostname+" ("+highest_ip+")" # print while browsing
          if call_for_every_device:             
            call_for_every_device(hostname, highest_ip, auth_token) # call specified function for every device, with hostname, ip and auth_token params

          devices_map[board_id] = {}
          devices_map[board_id]["hostname"] = hostname
          devices_map[board_id]["ip"] = highest_ip
          devices_map[board_id]["depths"] = deep
          devices_map[board_id]["children"] = []
        else:
          # loop found, break immediately
          raise(Exception("repeated board id '%s', hostname '%s'"%(board_id, hostname)))
      
        if not max_deep == 0: # if max deep limit set
          if deep == max_deep: 
            return board_id # enough this time, we do not dig deeper, smooth exit to parent call

        output = cisco.cmd("sh cdp neigh")
        body_flag = False
        neighbors = []
        for line in output.split("\n"):
          if not body_flag: # header in "sh cdp neigh" output
            m = re.search("Device\s+ID\s+Local\s+Intrfce\s+Holdtme\s+Capability\s+Platform\s+Port\s+ID", line, re.IGNORECASE)
            if m:
              body_flag = True
          else: # neighbors list
            m = re.search("^\s", line) # true if there is a wrap in line
            if not m:
              neighbor = re.sub(r"\s+.*$", "", line)
              neighbors.append(neighbor)
      
        for neighbor in neighbors: 
          output = cisco.cmd("sh cdp entry %s"%(neighbor)) # let's get deep into the neighbor
          m = re.search("platform\s*:\s*cisco", output, re.IGNORECASE|re.MULTILINE) # only cisco cdp neighbors
          if m:        
            m = re.search(r"ip address\s*:\s*(\d+\.\d+\.\d+\.\d+)", output, re.IGNORECASE|re.MULTILINE)
            if m:
              neighbor_ip = m.group(1)
              if neighbor_ip not in skip_neighbors:
                try:
                  # call myself for each neighbor (increase depths)
                  neighbor_board_id = browse_cisco_network(neighbor_ip, devices_map, skip_neighbors, new_auth_tokens, deep+1, max_deep, verbose, indent, call_for_every_device)
                  devices_map[board_id]["children"].append(neighbor_board_id) # no exception occured, so save the neighbor as a child
                except:
                  skip_neighbors.append(neighbor_ip) # bad neighbor, skip this ip next time if we meet it again

        return board_id # smooth exit for parent call
  else:
    raise(Exception("unable to log in to '%s'"%(host))) # no chance to authenticate, raise to parent call



def print_cisco_network(devices_map):
  """ This function draws network scheme hierarchically
  """
  def print_hierarchy(board_id, deep, indent):
    print indent*deep + devices_map[board_id]["hostname"] + " (" + devices_map[board_id]["ip"] + ")" # print current device
    for child_board_id in sorted(devices_map[board_id]["children"], key=lambda b_id: (len(devices_map[b_id]["children"]), devices_map[b_id]["hostname"])): # sort kids
      print_hierarchy(child_board_id, deep+1, indent) # call myself for the child

  root_border_id = sorted(devices_map.keys(), key=lambda b_id: devices_map[b_id]["depths"])[0] # looking for the root device
  print_hierarchy(root_border_id, 0, "\t") # let's start printing from the root

