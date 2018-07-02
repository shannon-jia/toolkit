# -*- coding: utf-8 -*-

"""Console script for read events configuration."""

import csv
import sys


events = []
events_sort = {}
event_segments = {}
events_dict = {}


def read_links_csv(filename='cam_links.csv'):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        try:
            for row in reader:
                events.append({
                    'event': int(row['event']),
                    'key_point': int(row['key_point']),
                    'camera': row['camera'],
                    'preset': int(row['preset']),
                    'unit': int(row['unit']),
                    'wing': row['cable'],
                    'system': int(row['system'])
                })
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    for _evt in events:
        system = _evt.get('system')
        unit = _evt.get('unit')
        wing = _evt.get('wing')
        key_point = _evt.get('key_point')
        _key = "{}_{}_{}".format(system, unit, wing)
        if _key not in events_dict:
            events_dict[_key] = [_evt]
            events_sort[_key] = [key_point]
        else:
            events_dict[_key].append(_evt)
            events_sort[_key].append(key_point)
            events_sort[_key].sort()

    for k, kp in events_sort.items():
        _min = 1
        event_segments[k] = []
        for _max in kp:
            event_segments[k].append((_min, _max))
            _min = _max + 1


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        fn = sys.argv[1]
        read_links_csv(fn)
    else:
        read_links_csv()
    from pprint import pprint
    pprint(event_segments)
