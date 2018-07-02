# -*- coding: utf-8 -*-

"""Console script for rps."""

import click
import csv
from pprint import pprint
from read_json import segments_dict, read_system_json
from read_csv import event_segments, events_dict, read_links_csv


@click.command()
@click.option('--segment', default='system.json',
              envvar='FN_SEGS',
              help='Display Segments File Name, json file')
@click.option('--event', default='cam_links.csv',
              envvar='FN_EVENT',
              help='Event Link Table File Name, csv file')
@click.option('--output', default='links.csv',
              envvar='FN_LINKS',
              help='Output File Name, csv file')
def main(segment, event, output):
    """Change Cable link table to Segments link table"""

    click.echo("See more documentation at http://www.mingvale.com")
    print("Open Json File: {} -------------------------".format(segment))
    read_system_json(segment)
    pprint(segments_dict)
    print("Open Csv File: {}---------------------------".format(event))
    read_links_csv(event)
    pprint(event_segments)
    cable_link = []

    print("Start to search......")
    for cable, segments in event_segments.items():
        for seg in segments:
            (_min, _max) = seg
            kp = events_dict.get(cable)
            for ik in kp:
                if _max == ik.get('key_point'):
                    camera = ik.get('camera')
                    preset = ik.get('preset')
                    break
            xl = search_display_segments(cable, _min, _max)
            if xl:
                print('Subcell {}:{} => {} ({}-{})'.format(cable, seg,
                                                           xl, camera, preset))
                for _it in xl:
                    _it.append(camera)
                    _it.append(preset)
                    cable_link.append(_it)
            else:
                print('!!!Subcell {}:{} => not match.'.format(cable, seg))

    print("Write Csv File: {}".format(output))
    with open(output, 'w') as csvfile:
        fieldnames = ['name', 'min', 'max', 'action', 'args']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for link in cable_link:
            writer.writerow({'name': link[0],
                             'min': link[1],
                             'max': link[2],
                             'action': 'CAM_'+str(link[3]),
                             'args': link[4]})


def search_display_segments(cable, v_min, v_max):
    _min = v_min
    _max = v_max
    _include_seg = []
    cable_segs = segments_dict.get(cable)
    if cable_segs is None:
        return None
    for seg in cable_segs:
        _start = seg.get('start', 1)
        _end = seg.get('end', 190)
        _name = seg.get('name')
        if _start > _end:
            _start, _end = _end, _start
        _range = range(_start, _end+1)
        if ((_min in _range) and (_max in _range)):
            _include_seg.append([_name, _min, _max])
            print("== {}".format(_range))
        elif ((_min in _range) and
              (_max not in _range)):
            print("=< {}".format(_range))
            _include_seg.append([_name, _min, _end])
            _min = _end + 1
        elif ((_min not in _range) and
              (_max in _range)):
            print("<= {}".format(_range))
            _include_seg.append([_name, _start, _max])
            _max = _start - 1
        elif ((_min < _start) and (_max > _end)):
            print(">< {}".format(_range))
            _include_seg.append([_name, _start, _end])
        else:
            print("!! {}".format(_range))

    if _include_seg:
        return _include_seg


if __name__ == '__main__':
    main()
