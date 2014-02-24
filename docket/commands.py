import os
import sys
import urlparse
import subprocess
import shutil
import contextlib

from os import makedirs
from os.path import exists, join, abspath, basename, dirname, islink

import dockerfile
import util
import platforms

__all__ = ['merge', 'generate']

RELDIR = "library"
ESPB_SCRIPT = "https://github.com/ack/espb/zipball/master"
SUPERVISED = "RUN echo '[program:{0}]\\ncommand={1}\\n\\n' > /etc/supervisor/conf.d/{2}.conf"

def merge(*refs, **kw):
    """pull/parse multiple dockerfiles, outputting to STDOUT """
    refs = list(refs)
    # resolve any remote references
    files = expand(*refs)
    # parse the dockerfiles
    parsed = parse(files)
    # ensure we can proceed
    errors = validate(parsed)
    if errors:
        for err in errors:
            print >> sys.stderr, err
        sys.exit(10)

    workspace = join(os.getcwd(), RELDIR)

    initial = parsed[0].parent
    print "########## docket intro"
    print "FROM {0}".format(initial)
    print

    # echo out the concatenated commands
    for df in parsed:
        for line in df.lines:
            print line

    if not kw.get('unsupervised'):
        print "\n\n########## docket outro"
        print "RUN mkdir -p /etc/supervisor/conf.d /var/log/supervisor"
        print "RUN touch /etc/supervisor/supervisord.conf"

        for df in parsed:
            startup = df.command
            if not startup:
                continue
            print SUPERVISED.format(df.name, startup, df.name)

        if kw.get('ssh'):
            print SUPERVISED.format('ssh', '/usr/sbin/sshd -D', 'ssh')

        print 'CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]'


def generate(name, parent, **kw):
    """
    create a docket Dockerfile
    """
    path = join('library', name)
    if exists(path):
       error("dir/file at path {0} exists!".format(path))

    override = None
    try:
        confpath = abspath("supervisord.conf")
        open(confpath)
    except IOError:
        confpath = abspath(join(dirname(__file__), "supervisord.conf"))

    os.makedirs(path)
    with util.chdir(path):
        shutil.copyfile(confpath, "supervisord.conf")

        with open("Dockerfile", 'w') as f:
            # this one (in practice) should be ignored
            print >> f, "FROM {0}".format(parent)
            # install supervisor and/or pip according to platform
            for dep in platforms.dependencies(parent):
                print >> f, "RUN {0}".format(dep)
            print >> f, "RUN mkdir -p /etc/supervisor"
            print >> f, "ADD supervisord.conf /etc/supervisor/supervisord.conf"
            print >> f, "ENV ETCD http://172.17.42.1:4001"

            if kw.get('inject'):
                print >> f, "# injected service pooling script"
                print >> f, "RUN pip install {0}".format(ESPB_SCRIPT)
                print >> f, 'CMD ["/usr/local/bin/espb", "register", "{0}"]'.format(name)

    print join(path, "Dockerfile")

def expand(*refs):
    """
    convert refs from { github-ref / directory / uri }
    to { local-directory }
    """
    files = []
    for ref in refs:
        if '.' == ref:
            ref = abspath(ref)
        local = join(RELDIR, ref)
        if not exists(local):
            local = resolve(ref)
        files.append(local)
    return files

def parse(files):
    parsed = []
    for path in files:
        df = dockerfile.Dockerfile(path)
        df.parse()
        parsed.append(df)
    return parsed


def validate(parsed):
    errors = []
    parents = ancestors(parsed)
    if len(parents) > 1:
        errors.append("Multiple ancestors detected: {0}".format(",".join(parents)))
    return errors


def ancestors(parsed):
    return set([f.parent for f in parsed])


def github(uri, outdir):
    if 'github.com' in uri:
        url = uri
    elif 'git@' in uri or 'git://' in uri:
        url = uri
    else:
        url = "https://github.com/" + uri
    out, err = subprocess.Popen(["git", "clone", url, outdir],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).communicate()
    print >> sys.stderr, out
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


def error(m, exit_code=1):
    print >> sys.stderr, m
    sys.exit(exit_code)
