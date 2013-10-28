from __future__ import division

import argparse

import robot
import digikey

parser = argparse.ArgumentParser()

def strip_right_F(s):
    s = s.rstrip()
    assert s.endswith('F')
    return s[:-1]

parser.add_argument('capacitance', metavar='CAPACITANCE', type=str, help='capacitance')
parser.add_argument('--tolerance', metavar='TOLERANCE', type=float, help='tolerance in percent (default: 10)', default=10)
parser.add_argument('--voltage', metavar='MINIMUM_VOLTAGE', type=float, help='minimum voltage (default: 10)', default=10)

args = parser.parse_args()


desired = digikey.parse_number(args.capacitance)


r = robot.Robot.start('http://www.digikey.com/product-search/en/capacitors/ceramic-capacitors')
fp = digikey.FilteringPage(r)

#print r.html

options = []
options.append(('quantity', 10))
options.append(('stock', 1))
options.append(('ColumnSort', 1000011)) # XXX does this change?
options.extend(fp.produce_filter_options('Capacitance',
    lambda s: digikey.within_tolerance(desired, args.tolerance, digikey.parse_number(s))))
options.extend(fp.produce_filter_options('Voltage - Rated',
    lambda s: digikey.parse_number(s) > args.voltage))
options.extend(fp.produce_filter_options('Package / Case',
    lambda s: s.strip().startswith('0603 ')))

url = r.get_new_url(options=options)
print url

r2 = robot.Robot.start(url)
rp = digikey.FilteringPage(r2)
print rp.first_part_number
