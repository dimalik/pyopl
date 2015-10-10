#! /usr/bin/env python
#
# Copyright (c) 2015, Dimitris Alikaniotis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of this package nor the
#   names of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# This software is provided by the copyright holders and contributors "as
# is" and any express or implied warranties, including, but not limited
# to, the implied warranties of merchantability and fitness for a
# particular purpose are disclaimed. In no event shall Dimitris Alikaniotis be
# liable for any direct, indirect, incidental, special, exemplary, or
# consequential damages (including, but not limited to, procurement of
# substitute goods or services; loss of use, data, or profits; or business
# interruption) however caused and on any theory of liability, whether in
# contract, strict liability, or tort (including negligence or otherwise)
# arising in any way out of the use of this software, even if advised of
# the possibility of such damage.
#
# (also known as the New BSD License)


import sys
import argparse
import urllib2

from engines.crossref import CrossRefEngine as CrossRef
from engines.arxiv import ArxivEngine as Arxiv

AVAILABLE_ENGINES = (
    CrossRef,
    Arxiv
)


def main(args=None):
    '''Called by commandline'''
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Python Online Paper Locator",
                                     prog="pyopl")
    parser.add_argument("-s", "--search", dest="search", action='store_true')
    parser.add_argument("-f", "--fetch", dest="search", action='store_false')
    parser.set_defaults(search=True)
    parser.add_argument("-e", "--engines", type=str,
                        help="Engines to query or get the citation from. If se\
arching then multiple engines can be given, but only one when given the identi\
fier.")
    parser.add_argument("-b", "--bib", default='', type=str,
                        help="The .bib file to save the citation to. If unspec\
ified then the STDOUT is used.")
    parser.add_argument("-n", "--secondary-bib", type=str, default=None,
                        help="A bibliography directory. If this is specified a\
 separate .bib file with a unique filename is going to be created at this loca\
tion.")
    parser.add_argument('key', nargs="+", type=str, help="Either you search qu\
ery or the paper identifier.")

    args = parser.parse_args(args)

    if args.engines:
        used_engines = [engine for engine in AVAILABLE_ENGINES
                        if engine._get_name() in args.engines]
    else:
        used_engines = AVAILABLE_ENGINES

    if args.search:
        query_results = []
        for engine in used_engines:
            try:
                query_engine = engine(' '.join(args.key))
                query_results.extend(query_engine.get_items())
            except urllib2.HTTPError:
                print "Engine: [{}] is down at the moment.".format(
                    engine._get_name())
        for query_item in query_results:
            print query_item
    else:
        engine = used_engines[0](args.key[0])
        engine.write_bib(bib_file=args.bib,
                         secondary_bib=args.secondary_bib)


if __name__ == '__main__':
    main()

