
COMMANDS = {
    'debian': [
        'which pip || apt-get install -qy python-pip',
        'apt-get install -qy supervisor'
        ],
    'redhat': [
        'which pip || (yum -y install python-setuptools && easy_install pip)',
        'sudo pip install supervisor'
        ],
    'unknown': [
        'which pip || curl -s https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python',
        'sudo pip install supervisor'
        ]
    }

def canonical(distro):
    if 'ubuntu' in distro or \
       'debian' in distro:
        return 'debian'
    if 'rhel' in distro or \
       'redhat' in distro or \
       'centos' in distro:
        return 'redhat'
    else:
        return 'unknown'

def dependencies(distro, **kw):
    return COMMANDS[canonical(distro)]

    
