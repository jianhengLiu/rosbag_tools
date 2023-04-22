#!/usr/bin/env python

import argparse
from fnmatch import fnmatchcase

from rosbag import Bag

import genpy


def main():

    parser = argparse.ArgumentParser(
        description='Merge one or more bag files with the possibilities of filtering topics.')
    parser.add_argument('outputbag',
                        help='output bag file with topics merged')
    parser.add_argument('inputbag', nargs='+',
                        help='input bag files')
    parser.add_argument('-v', '--verbose', action="store_true", default=False,
                        help='verbose output')
    parser.add_argument('-t', '--topics', default="*",
                        help='string interpreted as a list of topics (wildcards \'*\' and \'?\' allowed) to include in the merged bag file')

    args = parser.parse_args()

    topics = args.topics.split(' ')

    total_included_count = 0
    total_skipped_count = 0

    if (args.verbose):
        print("Writing bag file: " + args.outputbag)
        print("Matching topics against patters: '%s'" % ' '.join(topics))

    with Bag(args.outputbag, 'w') as o:
        for ifile in args.inputbag:
            matchedtopics = []
            included_count = 0
            skipped_count = 0
            if (args.verbose):
                print("> Reading bag file: " + ifile)
            with Bag(ifile, 'r') as ib:
                for topic, msg, t in ib:
                    if any(fnmatchcase(topic, pattern) for pattern in topics):
                        if not topic in matchedtopics:
                            matchedtopics.append(topic)
                            if (args.verbose):
                                print("Including matched topic '%s'" % topic)
                        # print("topic: '%s'" % topic)
                        print("\r", t, end="")

                        # check if msg has attribute 'header'
                        if (hasattr(msg, 'header')):
                            if (msg.header.stamp.to_sec() == 0):
                                o.write(
                                    topic, msg, genpy.Time.from_sec(t_not_zero))
                            else:
                                o.write(topic, msg, genpy.Time.from_sec(
                                    msg.header.stamp.to_sec()))
                                t_not_zero = msg.header.stamp.to_sec()
                        else:
                            # it is tf
                            if (msg.transforms[0].header.stamp.to_sec() == 0):
                                o.write(
                                    topic, msg, genpy.Time.from_sec(t_not_zero))
                            else:
                                o.write(topic, msg, genpy.Time.from_sec(
                                    msg.transforms[0].header.stamp.to_sec()))
                                t_not_zero = msg.transforms[0].header.stamp.to_sec(
                                )
                        included_count += 1
                    else:
                        skipped_count += 1
            total_included_count += included_count
            total_skipped_count += skipped_count
            if (args.verbose):
                print("< Included %d messages and skipped %d" %
                      (included_count, skipped_count))

    if (args.verbose):
        print("Total: Included %d messages and skipped %d" %
              (total_included_count, total_skipped_count))


if __name__ == "__main__":
    main()
