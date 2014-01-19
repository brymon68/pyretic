################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Srinivas Narayana (narayana@cs.princeton.edu)                        #
################################################################################
# Licensed to the Pyretic Project by one or more contributors. See the         #
# NOTICES file distributed with this work for additional information           #
# regarding copyright and ownership. The Pyretic Project licenses this         #
# file to you under the following license.                                     #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided the following conditions are met:       #
# - Redistributions of source code must retain the above copyright             #
#   notice, this list of conditions and the following disclaimer.              #
# - Redistributions in binary form must reproduce the above copyright          #
#   notice, this list of conditions and the following disclaimer in            #
#   the documentation or other materials provided with the distribution.       #
# - The names of the copyright holds and contributors may not be used to       #
#   endorse or promote products derived from this work without specific        #
#   prior written permission.                                                  #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT    #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the     #
# LICENSE file distributed with this work for specific language governing      #
# permissions and limitations under the License.                               #
################################################################################

################################################################################
# SETUP                                                                        #
# -------------------------------------------------------------------          #
# mininet: mininet.sh --topo=chain,2,2                                         #
# pyretic: pyretic.py pyretic.examples.path_query -m p0                        #
# test:    h1 ping h2 should produce packets at the controller from s2.        #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner
from pyretic.lib.path import *

import time
from datetime import datetime

ip1 = IPAddr('10.0.0.1')
ip2 = IPAddr('10.0.0.2')

def query_callback(pkt):
    print '**************'
    print 'Got a packet satisfying path query!'
    print pkt
    print '**************'

def path_test_1():
    a1 = atom(match(switch=1,srcip=ip1))
    a2 = atom(match(switch=2,dstip=ip2))
    p = a1 ^ a2
    p.register_callback(query_callback)
    return p

def path_main():
    return [path_test_1()]

def main():
    return (
        (match(srcip=ip1, dstip=ip2) >> ((match(switch=1) >> fwd(1)) + 
                                         (match(switch=2) >> fwd(2)))) +
        (match(srcip=ip2, dstip=ip1) >> ((match(switch=1) >> fwd(2)) +
                                         (match(switch=2) >> fwd(1))))
        )
