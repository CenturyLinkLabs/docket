
COMMANDS = {
    'debian': [
        'apt-get install -qy python-pip',
        'apt-get install -qy supervisor'
        ],
    'redhat': [
        'yum -y install python-setuptools',
        'easy_install pip'
        'sudo pip install supervisor'
        ],
    'unknown': [
        'curl -s https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python'
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

    
