# import urwid

import math
# import time

UPDATE_INTERVAL = 0.2

def sin100( x ):
    """
    A sin function that returns values between 0 and 100 and repeats
    after x == 100.
    """
    return 50 + 50 * math.sin( x * math.pi / 50 )


class GraphModel:
    """
    A class responsible for storing the data that will be displayed
    on the graph, and keeping track of which mode is enabled.
    """

    data_max_value = 100

    def __init__(self):
        data = [ ('Saw', range(0,100,2)*2),
            ('Square', [0]*30 + [100]*30),
            ('Sine 1', [sin100(x) for x in range(100)] ),
            ('Sine 2', [(sin100(x) + sin100(x*2))/2
                for x in range(100)] ),
            ('Sine 3', [(sin100(x) + sin100(x*3))/2
                for x in range(100)] ),
            ]
        self.modes = []
        self.data = {}
        for m, d in data:
            self.modes.append(m)
            self.data[m] = d

    def get_modes(self):
        return self.modes

    def set_mode(self, m):
        self.current_mode = m

    def get_data(self, offset, r):
        """
        Return the data in [offset:offset+r], the maximum value
        for items returned, and the offset at which the data
        repeats.
        """
        l = []
        d = self.data[self.current_mode]
        while r:
            offset = offset % len(d)
            segment = d[offset:offset+r]
            r -= len(segment)
            offset += len(segment)
            l += segment
        return l, self.data_max_value, len(d)

