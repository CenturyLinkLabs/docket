import os
import sys
import urlparse
import subprocess
import shutil
import contextlib

from os import makedirs
from os.path import exists, join, abspath, basename, dirname, islink

from . import dockerfile

RELDIR = "library"

__all__ = ['merge']

def merge(*refs):
    """pull/parse multiple dockerfiles, outputting to STDOUT """
    files, parsed = [], []
    # suck down any github refs
    for ref in refs:
        local = join(RELDIR, ref)
        if not exists(local):
            local = resolve(ref)
        files.append(local)

    workspace = join(os.getcwd(), RELDIR)
    for path in files:
        df = dockerfile.Dockerfile(path)
        df.parse()
        parsed.append(df)
        #df.mirror_files(workspace)

    # ensure we can proceed
    errors = validate(parsed)
    if errors:
        for err in errors:
            print >> sys.stderr, err
        sys.exit(10)

    initial = parsed[0].parent
    print "########## docket intro"
    print "FROM {0}".format(initial)
    print

    # echo out the concatenated commands
    for df in parsed:
        for line in df.lines:
            print line

    # assumed: user included some recipe that includes supervisor
    # maybe we can just "RUN pip install supervisor"?
    print "\n\n########## docket outro"
    print "RUN mkdir -p /etc/supervisor/conf.d /var/log/supervisor"
    print "RUN touch /etc/supervisor/supervisord.conf"
    template = "RUN echo '[program:{0}]\\ncommand={1}\\n\\n' > /etc/supervisor/conf.d/{2}.conf"
    for df in parsed:
        if not df.cmd:
            continue
        print template.format(df.name, df.command, df.name)
    print 'CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]'


def validate(dfiles):
    return []


def github(uri, outdir):
    if 'github.com' in uri:
        url = uri
    elif 'git@' in uri or 'git://' in uri:
        url = uri
    else:
        url = "https://github.com/" + parsed.path
    out, err = subprocess.Popen(["git", "clone", url, outdir],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()
    print out
    print >> sys.stderr, err

    
def resolve(ref):
    if exists(ref):
        # local directory already on disk
        return ref
    elif 'http' in ref and 'github.com' not in ref:
        # curl down a Dockerfile
        dir = basename(urlparse.urlparse(ref).path)
        target = join(RELDIR, dir)
        try: os.makedirs(target)
        except: pass
        with open(join(target, "Dockerfile")) as out:
            out.write(urllib.urlopen(ref))
        return target
    elif ref.lower().startswith("http://") or \
         ref.lower().startswith("https://") or \
         ref.lower().startswith("git") or \
         '/' in ref:
        dir = urlparse.urlparse(ref).path
        if dir.startswith('/'): dir = dir[1:]
        target = join(RELDIR, dir)
        if not exists(target):
            try: makedirs(target)
            except: pass
            github(ref, target)
        return target
    else:
        raise Exception("unknown path type: {0}".format(ref))
