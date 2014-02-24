#!/usr/bin/env python

import sys
import optparse
import dockerfile
import commands

USAGE = """docket [options] <command> [args]

Dockerfile wrapping paper.
commands:

  generate - create a new Docketfile to bind entire container together
     arg1: project name (creates library/<name>/Dockerfile etc)
     arg2: ancestor Dockerfile (should be shared across all merged Dockerfiles)

  merge - merge collapsed Dockerfiles
     args: (multiple) paths/refs to Dockerfiles

"""

def main():
    op = optparse.OptionParser(usage=USAGE)
    op.add_option('-V', '--verbose')
    op.add_option('-U', '--unsupervised', help="disable supervisor integration", action="store_true", default=False)
    op.add_option('-i', '--inject', help="inject espb script for service pooling", action="store_true", default=False)
    op.add_option('-s', '--ssh', help="enable sshd in merged container", action="store_true", default=False)

    opt, args = op.parse_args()
    if not args:
        print >> sys.stderr, USAGE
        sys.exit(1)

    cmd = args.pop(0)
    fn = getattr(commands, cmd)
    if not fn:
        print >> sys.stderr, usage
        sys.exit(1)

    kw = dict((k, getattr(opt, k)) for k in ['inject', 'ssh', 'unsupervised'])
    fn(*args, **kw)
    sys.exit(0)
