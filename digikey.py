from __future__ import division


def parse_number(s):
    s = s.strip()
    multipliers = dict(k=1e3, M=1e6, G=1e9)
    mult = 1
    while s[-1] in multipliers:
        mult *= multipliers[s[-1]]
        s = s[:-1]
    return float(s) * mult

def within_tolerance(desired, tolerance_percent, actual):
    return abs(actual - desired)/desired <= tolerance_percent/100

class FilteringPage(object):
    def __init__(self, r):
        form = r.html.find('form', dict(name='attform'))
        table = form.table
        params = [th.string for th in table.tr.findAll('th')]
        print params

        selects = [td.select for td in table.tr.findNextSibling().findAll('td', recursive=False)]
        assert len(selects) == len(params)
        
        self.params = params
        self.selects = selects

    def produce_filter_options(self, name, func):
        i = self.params.index(name)
        sel = self.selects[i]
        res = [(sel['name'], option['value'])
            for option in sel.findAll('option', recursive=False)
            if func(option.string)]
        if not res:
            assert False, 'filter matched nothing'
        return res
