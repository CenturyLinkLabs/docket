import os
import string
import json
import contextlib
import shutil
from os.path import abspath, join, exists, basename, islink

@contextlib.contextmanager
def chdir(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(prev_cwd)


class Dockerfile:
    """
    parser/interpreter for Dockerfiles, extracting a selection of fields
    """
    
    def __init__(self, path):
        self.path = path
        self.name = basename(path) if '/' in path else path
        for attr in ['from', 'cmd', 'entrypoint', 'env']:
            setattr(self, attr, None)
        self.lines = []
        self.paths = []
        self.env = []
        self.volumes = []
        self.ports = []

    def parse(self):
        with chdir(self.path):
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
                        continue
                    if token == 'cmd':
                        if 'supervisord' in text:
                            print >> sys.stderr, "!! dropping supervisord invocation from {0}".format(self.path)
                        else:
                            self.cmd = text
                        continue
                    if token == 'entrypoint':
                        #self.entrypoint = text
                        continue
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
        return " ".join(json.loads(self.cmd))
                    
        
