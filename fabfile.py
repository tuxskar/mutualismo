from __future__ import with_statement

from fabric.api import env, cd, run, sudo, local
from fabric.contrib.console import confirm
from fabric.colors import cyan, red


env.hosts        = ['mutualismo.es']
env.forge_path   = '/usr/share/trac/projects/mutualismo'
env.repo_path    = '/home/git'
env.repositories = ['Mutualismo']


def _read_cmd(prompt=None):
    if prompt is None:
        prompt = 'Command to run: '
    return raw_input(cyan(prompt)).strip()

def cmd(cmd=''):
    """"Run a command in ``path``. Usable from other commands or CLI."""
    if not cmd:
        cmd = _read_cmd()
    if cmd:
        run(cmd)

def sdo(cmd=''):
    """Sudo a command in ``path``. Usable from other commands or CLI."""
    if not cmd:
        cmd = _read_cmd()
    if cmd:
        sudo(cmd)

def trac(cmd=''):
    """"
    Execute a ``trac-admin`` command in the forge path. Usable from other 
    commands or CLI.
    """
    if not cmd:
        cmd = _read_cmd('Insert trac command: ')
    if cmd:
        with cd(env.forge_path):
            trac_admin_cmd = ' '.join(['trac-admin . ', cmd]) 
            sudo(trac_admin_cmd)  

def aptitude():
    """"Execute an ``aptitude`` command. Usable from other commands or CLI."""
    cmd = _read_cmd('Insert an aptitude command: ')
    if cmd:
        aptitude = ' '.join(['aptitude', cmd])
        run(aptitude)

def apt_get():
    """"Execute an ``apt-get`` command. Usable from other commands or CLI."""
    cmd = _read_cmd('Insert an apt-get command: ')
    if cmd:
        apt_get_cmd = ' '.join(['apt-get', cmd])
        sudo(apt_get_cmd)

def resync_repos(repo=''):
    """Resyncs repos with Trac."""
    for repo in env.repositories:
        cmd  = ' '.join(['repository resync', repo])
        trac(cmd)

def restart():
    """Restart the server."""
    if confirm(red('Are you sure that you want to restart the server?')):
        sudo('apache2ctl restart', pty=True)

def svn():
    """Mirrors the current repository state with the svn repository."""
    local("git checkout svn")
    local("git svn dcommit")
    local("git merge master")
    local("git checkout master")

# Local tasks
def clean():
    """Remove all .pyc files."""
    local('find . -name "*.pyc" -exec rm {} \;')

def debug():
    """Find files with debug symbols."""
    clean()
    local('grep -ir "print" *')
    local('grep -ir "console.log" *')

def todo():
    """Find all TODO and XXX."""
    clean()
    local('grep -ir "TODO" *')
    local('grep -ir "XXX" *')
