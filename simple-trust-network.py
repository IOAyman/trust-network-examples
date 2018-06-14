#!/bin/env python
from optparse import OptionParser
from random import choice

from net_flow import TrustNetwork


# Prepare the script options
parser = OptionParser(usage='%prog [options] DATA_FILE')
parser.add_option('-o', '--output',
                  action='store', dest='output',
                  help='File to save results to [default: %default]')
options, args = parser.parse_args()
if len(args) != 1:
  parser.error('A source data file must be supplied!')

# Network capacities
capacities = [3200, 800, 200, 50, 12, 4, 2, 1]
# Create a new empty network. Seed node is '-'
network = TrustNetwork()

# Open source data file
with open(args[0], 'r') as f:
  for line in f.readlines():
    # Exclude commented lines
    if line and not line.startswith('#'):
      # Parse nodes
      from_node, to_node, level = line.strip().split(',')
      # Create edge
      network.add_edge(from_node, to_node)

# Randomly select some nodes to start with
starting_nodes = [choice(network) for i in xrange(3)]
for node in starting_nodes: network.add_edge('-', node)

# Calculate the flow
network.calculate(capacities)

# Save results to output file if specified
if options.output:
  print 'Saving results to %s' % options.output
  with open(options.output, 'w') as f:
    f.writelines(['%s,%s\n' % (user, network.is_auth(user)) for user in network])

else: # Print results otherwise
  print "%s\t%s" % ('user', 'is_trusted')
  for user in network:
    print "%-10s\t%s" % (user, network.is_auth(user))

# Print stats
print """
Total users %d
Trusted users %d
Untrusted users %d
""" % (
  len(network),
  len([user for user in network if network.is_auth(user)]),
  len([user for user in network if not network.is_auth(user)])
)
