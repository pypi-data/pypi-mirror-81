from __future__ import unicode_literals
import os
from pkg_resources import Requirement, resource_filename, ResolutionError
import shutil
import stat
import sys
from tempfile import mkdtemp
import traceback

from distutils import dir_util
from pytest import fixture
import psutil

from doit.cmd_base import TaskLoader
from doit.doit_cmd import DoitMain
from doit.dependency import Dependency, DbmDB

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

N_THREADS = list(set([1, 2, psutil.cpu_count(logical = False)]))

@fixture(scope='session')
def datadir(request):
    '''
    Fixture responsible for locating the test data directory and copying it
    into a temporary directory.
    '''
    test_dir = os.path.dirname(__file__)
    data_dir = os.path.join(test_dir, 'data')

    def getter(filename):
        filepath = os.path.join(os.getcwd(), filename)
        shutil.copyfile(os.path.join(data_dir, filename),
                        filepath)
        return filepath

    return getter


def check_status(task, tasks=None, dep_file='.doit.db'):
    if tasks is None:
        tasks = [task]
    mgr = Dependency(DbmDB, os.path.abspath(dep_file))
    status = mgr.get_status(task, tasks)
    return status


def run_tasks(tasks, args, config={'verbosity': 0}):
    
    if type(tasks) is not list:
        raise TypeError('tasks must be a list')
   
    class Loader(TaskLoader):
        @staticmethod
        def load_tasks(cmd, opt_values, pos_args):
            return tasks, config
    print('DOIT: RUN TASKS')
    return DoitMain(Loader()).run(args)


def run_task(task, cmd='run', verbosity=0):
    return run_tasks([task], [cmd], config={'verbosity': verbosity})


def touch(filename):
    '''Perform the equivalent of bash's touch on the file.

    Args:
        filename (str): File path to touch.
    '''

    open(filename, 'a').close()
    os.chmod(filename, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)



'''
These script running functions were taken from the khmer project:
https://github.com/dib-lab/khmer/blob/master/tests/khmer_tst_utils.py
'''

def scriptpath(scriptname='shmlast'):
    "Return the path to the scripts, in both dev and install situations."

    path = os.path.join(os.path.dirname(__file__), "../../bin")
    if os.path.exists(os.path.join(path, scriptname)):
        return path

    path = os.path.join(os.path.dirname(__file__), "../../../EGG-INFO/bin")
    if os.path.exists(os.path.join(path, scriptname)):
        return path

    for path in os.environ['PATH'].split(':'):
        if os.path.exists(os.path.join(path, scriptname)):
            return path


def _runscript(scriptname):
    """
    Find & run a script with exec (i.e. not via os.system or subprocess).
    """

    import pkg_resources
    ns = {"__name__": "__main__"}
    ns['sys'] = globals()['sys']

    try:
        pkg_resources.get_distribution("shmlast").run_script(scriptname, ns)
        return 0
    except pkg_resources.ResolutionError as err:
        path = scriptpath()

        scriptfile = os.path.join(path, scriptname)
        if os.path.isfile(scriptfile):
            if os.path.isfile(scriptfile):
                exec(compile(open(scriptfile).read(), scriptfile, 'exec'), ns)
                return 0

    return -1


def runscript(scriptname, args, directory=None,
              fail_ok=False, sandbox=False):
    """Run a Python script using exec().
    Run the given Python script, with the given args, in the given directory,
    using 'exec'.  Mimic proper shell functionality with argv, and capture
    stdout and stderr.
    When using :attr:`fail_ok`=False in tests, specify the expected error.
    """
    sysargs = [scriptname]
    sysargs.extend(args)
    cwd = os.getcwd()

    try:
        status = -1
        oldargs = sys.argv
        sys.argv = sysargs

        oldout, olderr = sys.stdout, sys.stderr
        sys.stdout = StringIO()
        sys.stdout.name = "StringIO"
        sys.stderr = StringIO()

        if directory:
            os.chdir(directory)
        else:
            directory = cwd

        try:
            print('running:', scriptname, 'in:', directory, file=oldout)
            print('arguments', sysargs, file=oldout)

            status = _runscript(scriptname)
        except SystemExit as e:
            status = e.code
        except:
            traceback.print_exc(file=sys.stderr)
            status = -1
    finally:
        sys.argv = oldargs
        out, err = sys.stdout.getvalue(), sys.stderr.getvalue()
        sys.stdout, sys.stderr = oldout, olderr

        os.chdir(cwd)

    if status != 0 and not fail_ok:
        print('Script Failed:', scriptname, 
              'Status:', status, 
              'Output:', out,
              'Error:', err,
              sep='\n')
        assert False

    return status, out, err


def run_shell_cmd(cmd, fail_ok=False, in_directory=None):
    cwd = os.getcwd()
    if in_directory:
        os.chdir(in_directory)

    print('running: ', cmd)
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        (out, err) = p.communicate()

        out = out.decode('utf-8')
        err = err.decode('utf-8')

        if p.returncode != 0 and not fail_ok:
            print('out:', out)
            print('err:', err)
            raise AssertionError("exit code is non zero: %d" % p.returncode)

        return (p.returncode, out, err)
    finally:
        os.chdir(cwd)

