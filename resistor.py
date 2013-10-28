from __future__ import division

import argparse

import robot
import digikey

parser = argparse.ArgumentParser()

parser.add_argument('resistance', metavar='RESISTANCE', type=str, help='resistance')
parser.add_argument('--tolerance', metavar='TOLERANCE', type=float, help='tolerance in percent (default: 1)', default=1)

args = parser.parse_args()


r = robot.Robot.start('http://www.digikey.com/product-search/en/resistors/chip-resistor-surface-mount')
fp = digikey.FilteringPage(r)

#print r.html


options = []
options.append(('quantity', 10))
options.append(('stock', 1))
options.append(('ColumnSort', 1000011)) # XXX does this change?
options.extend(fp.produce_filter_options('Resistance (Ohms)',
    lambda s: digikey.within_tolerance(digikey.parse_number(args.resistance), args.tolerance, digikey.parse_number(s))))
options.extend(fp.produce_filter_options('Package / Case',
    lambda s: s.strip().startswith('0603 ')))

url = r.get_new_url(options=options)
print url

r2 = robot.Robot.start(url)
rp = digikey.FilteringPage(r2)
print rp.first_part_number
