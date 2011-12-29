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

def _read_args(cmd=None):
    if cmd is None:
        cmd = _read_cmd()
    if cmd:
        args = _read_cmd('Arguments for %s: ' %cmd)

    if cmd and args:
        return ' '.join([cmd, args])

def cmd(cmd=''):
    """"Run a command. Usable from other commands or CLI."""
    if not cmd:
        cmd = _read_cmd()
    if cmd:
        run(cmd)

def sdo(cmd=''):
    """Sudo a command. Usable from other commands or CLI."""
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
    cmd = _read_args('aptitude')
    if cmd:
        sudo(cmd)

def apt_get():
    """"Execute an ``apt-get`` command. Usable from other commands or CLI."""
    cmd = _read_args('apt-get')
    if cmd:
        sudo(cmd)

def resync_repos(repo=''):
    """Resyncs repos with Trac."""
    for repo in env.repositories:
        cmd  = ' '.join(['repository resync', repo])
        trac(cmd)

def reload_nginx():
    """Reload the server."""
    if confirm(red('Are you sure that you want to reload the server?')):
        sudo('nginx -s reload', pty=True)

def reload_tracd():
    """Reload Trac server."""
    if confirm(red('Are you sure that you want to reload the server?')):
        sudo('kill -9 `cat /var/run/tracd/tracd.pid`', pty=True)
        sudo('invoke-rc.d tracd start')

def svn():
    """Mirrors the current repository state with the svn repository."""
    local("git checkout svn")
    print '>> Fetching latest changes on the svn repo'
    local("git svn fetch")
    local("git svn rebase")
    print '>> Merging svn repo with master branch'
    local("git merge master")
    print '>> Comitting to svn repo'
    local("git svn dcommit")
    local("git checkout master")

def github():
    """Mirrors the current repository state with the svn repository."""
    local("git push -u github master")

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
