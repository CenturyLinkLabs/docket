import os
import sys
import string
import json
import shutil
from os.path import abspath, join, exists, basename, dirname, islink

import util

class Dockerfile:
    """
    parser/interpreter for Dockerfiles, extracting a selection of fields
    """
    
    def __init__(self, path):
        self.path = path
        if '/' in path:
            self.name = basename(path) or basename(dirname(path))
        else:
            self.name = path
        for attr in ['from', 'cmd', 'entrypoint', 'env']:
            setattr(self, attr, None)
        self.lines = []
        self.paths = []
        self.env = []
        self.volumes = []
        self.ports = []

    def parse(self):
        with util.chdir(self.path):
            with open("Dockerfile") as f:
                self.lines.append("\n\n########## {0}".format(self.name))
                for line in map(string.strip, f.readlines()):
                    try:
                        tokens = line.strip().split()
                        token = tokens.pop(0).lower()
                        text = " ".join(tokens)
                    except (IndexError, AttributeError):
                        continue
                    if token == 'from':
                        self.parent = text
                        #line = "##" + line
                        continue
                    if token == 'cmd':
                        if 'supervisord' in text:
                            print >> sys.stderr, "!! dropping supervisord invocation from {0}".format(self.path)
                        else:
                            self.cmd = text
                        line = "#% " + line
                    if token == 'entrypoint':
                        self.entrypoint = text
                        line = "#% " + line
                    if token == 'add':
                        # rewrite line with qualified path
                        src, dst = text.split()
                        rewritten = join(self.path, src)
                        self.paths.append(rewritten)
                        line = "ADD {0} {1}".format(rewritten, dst)
                    if token == 'env':
                        self.env.append(text)
                    if token == 'volume':
                        self.volumes.append(text)
                    if token == 'expose':
                        self.ports.extend(text.split())

                    self.lines.append(line)

    @property
    def command(self):
        val = None
        if self.cmd and self.entrypoint:
            # use cmd?
            val = self.cmd
        elif self.cmd and not self.entrypoint:
            val = self.cmd
        elif self.entrypoint:
            val = self.entrypoint
        else:
            val = self.cmd
        if val:
            return " ".join(json.loads(val))
                    
        
