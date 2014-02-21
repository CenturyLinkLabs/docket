#!/usr/bin/env python

import sys
import optparse
from . import dockerfile
from . import commands

def main():
    usage = "usage: docket [options] <command>"
    op = optparse.OptionParser(usage=usage)
    op.add_option('-V', '--verbose')
    opt, args = op.parse_args()
    if not args:
        print >> sys.stderr, usage
        sys.exit(1)

    cmd = args.pop(0)
    fn = getattr(commands, cmd)
    if not fn:
        print >> sys.stderr, usage
        sys.exit(1)

    fn(*args)
    sys.exit(0)
