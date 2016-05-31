#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

nodes, vBucketsNR = 1, 4096
vBuckets = [nodes] * vBucketsNR
while nodes <= 16:
    print min(vBucketsNR * 2, 256) * "-"
    nodes += 1
    newAdd = [nodes] * (vBucketsNR / nodes)
    canBeAssgined = []
    for i in range(1, nodes):
		# calculate every exist node's assignment slots(bucket)
        canBeAssgined.append(vBucketsNR / (nodes - 1) - (vBucketsNR / nodes))

    s = len(vBuckets)

	# for balance the bucket distribution we iterate all buckets
	# randomly. actually start from head or tail
    seq = range(0, s) if nodes % 2 == 0 else range(s - 1, 0, -1)

    for index in seq:
        if len(newAdd) == 0:
            break
        if canBeAssgined[vBuckets[index] - 1] != 0:
            canBeAssgined[vBuckets[index] - 1] = canBeAssgined[vBuckets[index] - 1] - 1
            vBuckets[index] = newAdd.pop()

    for i in range(0, len(vBuckets)):
        sys.stdout.write("%d " % vBuckets[i])
    print ""

    sum = []
    for i in range(1, nodes + 1):
        sum.append(vBuckets.count(i))
    print "After add indexed node %d => %s" % (len(sum), sum)
