# -*- coding: utf-8 -*-

"""Console script for read system display segments configuration."""

import json
import sys
segments_list = []
segments_dict = {}
modules_dict = {}


def read_system_json(filename='system.json'):
    with open(filename) as data_file:
        try:
            data = json.load(data_file)
        except TypeError:
            sys.exit('Error on load json file.')

        for line in data['system']:
            line_no = int(line['line'])
            segments = line['display_segments']
            for seg in segments:
                if seg['unit'] == 0:
                    continue
                name = 'SEG_' + str(line_no) + '_' + str(seg['seg_no'])
                seg['name'] = name
                seg['system'] = line_no
                segments_list.append(seg)

            modules = line['modules']
            _mods_list = []
            for mod in modules:
                if mod['state'] != 'Running':
                    continue
                _mods_list.append(mod.get('name'))
            modules_dict[line_no] = _mods_list

        for seg in segments_list:
            system = seg.get('system')
            unit = seg.get('unit')
            wing = seg.get('wing')
            name = seg.get('name')
            start = seg.get('start')
            end = seg.get('end')
            _key = "{}_{}_{}".format(system, unit, wing)
            x_seg = {
                'name': name,
                'start': start,
                'end': end
            }
            if _key not in segments_dict:
                segments_dict[_key] = [x_seg]
            else:
                segments_dict[_key].append(x_seg)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        fn = sys.argv[1]
        read_system_json(fn)
    else:
        read_system_json()
    from pprint import pprint
    pprint(segments_dict)
    # pprint(segments_list)
    pprint(modules_dict)
