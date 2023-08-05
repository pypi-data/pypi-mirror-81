# Copyright 2019 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
import shutil
import sys
import subprocess
import pytest
from portmod.repo.loader import __load_file
from portmod.globals import env
from portmod.main import pybuild_manifest
from .env import setup_env, tear_down_env
import pybuild_
from portmod.mod import src_prepare, src_unpack

TMP_REPO = os.path.join(os.path.dirname(env.TMP_DIR), "not-portmod")
TMP_FILE = os.path.join(TMP_REPO, "test", "test", "test-1.0.pybuild")
env.ALLOW_LOAD_ERROR = False


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def create_pybuild(filestring):
    os.makedirs(env.TMP_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(TMP_FILE), exist_ok=True)
    os.makedirs(os.path.join(TMP_REPO, "profiles"), exist_ok=True)

    with open(TMP_FILE, "w") as file:
        file.write(filestring)

    with open(os.path.join(TMP_REPO, "profiles", "repo_name"), "w") as file:
        file.write("test")

    with open(os.path.join(TMP_REPO, "profiles", "categories"), "w") as file:
        file.write("test")

    pybuild_manifest(TMP_FILE)


def cleanup_tmp():
    shutil.rmtree(TMP_REPO)


def test_safe():
    """Tests that a simple safe pybuild loads correctly"""
    file = """
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    create_pybuild(file)
    __load_file(TMP_FILE)
    cleanup_tmp()


def test_write_globalscope():
    """Tests that writing to files outside TMP_DIR is forbidden in the global scope"""
    file = f"""
import os
from pybuild import Pybuild1

os.remove("{TMP_FILE}")

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(PermissionError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_write_globalscope_2():
    """Tests that writing to files within TMP_DIR is forbidden in the global scope"""
    file = f"""
import os
from pybuild import Pybuild1

os.remove("{env.TMP_DIR}")

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(PermissionError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_read_globalscope():
    """Tests that reading from files outside TMP_DIR is forbidden in the global scope"""
    file = f"""
import os
from pybuild import Pybuild1

os.path.exists("{TMP_FILE}")

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(PermissionError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_read_globalscope_2():
    """Tests that reading from files within TMP_DIR is forbidden in the global scope"""
    file = f"""
import os
from pybuild import Pybuild1

os.path.exists("{env.TMP_DIR}")

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(PermissionError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_read_src_unpack():
    """Tests that reading from files outside TMP_DIR is forbidden within src_unpack"""
    file = f"""
import os
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        os.path.exists("{TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        src_unpack(mod, env.TMP_DIR)
    cleanup_tmp()


def test_write_src_unpack():
    """Tests that writing to files outside TMP_DIR is forbidden within src_unpack"""
    file = f"""
import os
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        os.remove("{TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        src_unpack(mod, env.TMP_DIR)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_read_can_update_live():
    """
    Tests that reading from files outside TMP_DIR is forbidden within can_update_live
    """
    file = f"""
import os
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def can_update_live(self):
        os.path.exists("{TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        mod.can_update_live()
    cleanup_tmp()


def test_write_can_update_live():
    """
    Tests that writing to files outside TMP_DIR is forbidden within can_update_live
    """
    file = f"""
import os
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def can_update_live(self):
        os.remove("{TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        mod.can_update_live()
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_read_src_prepare():
    """Tests that reading from files outside TMP_DIR is allowed within src_prepare"""
    file = f"""
import os
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        os.path.exists("{TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_write_src_prepare():
    """Tests that writing to files outside TMP_DIR is not allowed within src_prepare"""
    file = f"""
import os
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        os.remove("{TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        src_prepare(mod, env.TMP_DIR)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_formatstr():
    """Tests that string.format is banned"""
    file = """
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="{}".format("Test")
    LICENSE="GPL-3"
"""
    with pytest.raises(NotImplementedError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    cleanup_tmp()


def test_module_write_1():
    """Tests that modules are not modifiable from within pybuilds"""
    file = """
import pybuild

pybuild.Pybuild1 = str

class Mod(pybuild.Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(AttributeError):
        create_pybuild(file)
        __load_file(TMP_FILE)

    file = """
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    create_pybuild(file)
    __load_file(TMP_FILE)
    cleanup_tmp()


def test_module_write_2():
    """Tests that module changes do not propagate from within pybuilds"""
    file = """
import sys
from pybuild import Pybuild1

sys.platform = "foo"

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    old_platform = sys.platform
    create_pybuild(file)
    __load_file(TMP_FILE)
    assert sys.platform == old_platform
    cleanup_tmp()


def test_module_write_3():
    """Tests that module subattribute changes do not propagate from within pybuilds"""
    file = """
import pybuild
from pybuild import Pybuild1

pybuild.Pybuild1.src_install = "foo"

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    create_pybuild(file)
    __load_file(TMP_FILE)
    assert pybuild_.Pybuild1.src_install != "foo"
    cleanup_tmp()


def test_module_unsafe_import():
    """Tests that modules cannot be imported indirectly"""
    file = """
from typing import sys
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(SyntaxError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    cleanup_tmp()


def test_module_unsafe_import_2():
    """Tests that modules cannot be accessed indirectly"""
    file = """
import json
from pybuild import Pybuild1

assert json.codecs is not None

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(AssertionError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    cleanup_tmp()


def test_submodule_function():
    """Tests that whitelisted submodules can be used properly"""
    file = """
import os
from pybuild import Pybuild1

FOO = os.path.join("Foo", "Bar")

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    create_pybuild(file)
    __load_file(TMP_FILE)
    cleanup_tmp()


def test_underscore():
    """Tests that we can't access names beginning with underscores"""
    file = """
import os
from pybuild import Pybuild1

os.path.join.__globals__

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(SyntaxError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    cleanup_tmp()


def test_getattr():
    """Tests that we can't use getattr to access names beginning with underscores"""
    file = """
import os
from pybuild import Pybuild1

getattr(os.path.join, "__globals__")

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(AttributeError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    cleanup_tmp()


def test_execute():
    """Tests that we can execute files properly even if we fiddle with platform"""
    file = """
from pybuild import Pybuild1
import sys

# If this affected the scope of execute, this would
# raise an unsupported platform exception
origplatform = sys.platform
sys.platform = "foo"

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        if origplatform == "win32":
            self.execute("dir")
        else:
            self.execute("ls")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_execute_src_prepare_write():
    """Tests that we can't modify files through execute in src_prepare"""
    file = f"""
from pybuild import Pybuild1
import sys

# If this affected the scope of execute, this would
# raise an unsupported platform exception
origplatform = sys.platform
sys.platform = "foo"

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        if origplatform == "win32":
            self.execute('cmd /c "del {TMP_FILE}"')
        else:
            self.execute("rm {TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    if sys.platform == "win32":
        # Sandboxie won't cause an error when deleting the file fails
        src_prepare(mod, env.TMP_DIR)
    else:
        with pytest.raises(subprocess.CalledProcessError):
            src_prepare(mod, env.TMP_DIR)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


@pytest.mark.xfail(
    sys.platform == "win32" and "APPVEYOR" in os.environ,
    reason="Sandboxie doesn't behave quite as we expect it to",
    raises=subprocess.CalledProcessError,
)
def test_execute_src_prepare_read():
    """Tests that we can read files through execute in src_prepare"""
    file = f"""
from pybuild import Pybuild1
import sys

# If this affected the scope of execute, this would
# raise an unsupported platform exception
origplatform = sys.platform
sys.platform = "foo"

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        if origplatform == "win32":
            self.execute('dir "{TMP_FILE}"')
        else:
            self.execute("ls {TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


@pytest.mark.xfail(
    sys.platform == "win32" and "APPVEYOR" in os.environ,
    reason="Sandboxie doesn't behave quite as we expect it to",
)
def test_execute_src_unpack_read():
    """Tests that we can't read files through execute in src_unpack"""
    file = f"""
from pybuild import Pybuild1
import sys

# If this affected the scope of execute, this would
# raise an unsupported platform exception
origplatform = sys.platform
sys.platform = "foo"

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        if origplatform == "win32":
            self.execute('dir "{TMP_FILE}"')
        else:
            self.execute("ls {TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(subprocess.CalledProcessError):
        src_unpack(mod, env.TMP_DIR)
    cleanup_tmp()


@pytest.mark.xfail(
    sys.platform == "win32",
    reason="Unknown failure related to Sandboxie",
    raises=subprocess.CalledProcessError,
)
def test_execute_network_permissions():
    """Tests that network permissions work in src_unpack but not src_prepare"""
    file = """
from pybuild import Pybuild1
import sys

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        if sys.platform == "win32":
            self.execute('ping /n 1 1.1.1.1')
        else:
            self.execute('curl 1.1.1.1')

    def src_prepare(self):
        if sys.platform == "win32":
            self.execute('ping /n 1 1.1.1.1')
        else:
            self.execute('curl 1.1.1.1')
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_unpack(mod, env.TMP_DIR)
    with pytest.raises(subprocess.CalledProcessError):
        src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_execute_permissions_bleed():
    """Tests that network permissions from src_unpack don't bleed into src_prepare"""
    file = f"""
from pybuild import Pybuild1
import sys

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        if sys.platform == "win32":
            self.execute('dir "{env.TMP_DIR}"')
        else:
            self.execute("ls {env.TMP_DIR}")

    def src_prepare(self):
        if sys.platform == "win32":
            self.execute('ping /n 1 gitlab.com')
        else:
            self.execute('curl https://gitlab.com')
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_unpack(mod, env.TMP_DIR)
    with pytest.raises(subprocess.CalledProcessError):
        src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_default():
    """Tests that wrapped functions with default arguments work properly"""
    file = """
from pybuild import Pybuild1
import os


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        os.listdir()
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_execute_escape():
    """Tests that you can't escape from execute"""
    file = f"""
from pybuild import Pybuild1
import sys


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        if sys.platform == "win32":
            self.execute('& del "{TMP_FILE}"')
        else:
            self.execute("; rm {TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(subprocess.CalledProcessError):
        src_prepare(mod, env.TMP_DIR)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_execute_escape_2():
    """Tests that you can't escape from execute"""
    file = f"""
from pybuild import Pybuild1
import sys


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        if sys.platform == "win32":
            self.execute('"& cmd /c "del {TMP_FILE}"')
        else:
            self.execute("; rm {TMP_FILE}")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises((subprocess.CalledProcessError, ValueError)):
        src_prepare(mod, env.TMP_DIR)
    assert os.path.exists(TMP_FILE)
    cleanup_tmp()


def test_safe_open_global():
    """Tests that you can't use open in the global scope"""
    file = f"""
from pybuild import Pybuild1

with open("{TMP_FILE}", "r") as file:
    file.read()

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"
"""
    with pytest.raises(PermissionError):
        create_pybuild(file)
        __load_file(TMP_FILE)
    cleanup_tmp()


def test_safe_open_src_unpack():
    """Tests that you can't use open in src_unpack"""
    file = f"""
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        with open("{TMP_FILE}", "r") as file:
            file.read()
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        src_unpack(mod, env.TMP_DIR)
    cleanup_tmp()


def test_safe_open_src_prepare():
    """Tests that you can't write outside tmpdir with open in src_prepare"""
    file = f"""
from pybuild import Pybuild1


class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        with open("{TMP_FILE}", "w") as file:
            print("foo", file=file)
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    with pytest.raises(PermissionError):
        src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_safe_open_allowed():
    """Tests situations where you can use open"""
    file = f"""
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        with open("{TMP_FILE}", "r") as file:
            file.read()
        with open("{env.TMP_DIR}/foofile", "w") as file:
            print("foo", file=file)

    def src_unpack(self):
        with open("{env.TMP_DIR}/foofile", "w") as file:
            print("foo", file=file)
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_unpack(mod, env.TMP_DIR)
    src_prepare(mod, env.TMP_DIR)
    os.remove(f"{env.TMP_DIR}/foofile")
    cleanup_tmp()


def test_fake_perms():
    """Tests that Permissions cannot be declared in functions that use default permissions"""
    file = f"""
import os
from pybuild import Pybuild1

class Foo:
    pass

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def can_update_live(self):
        __PERMS = Foo()
        __PERMS.global_read = True
        os.path.exists("{TMP_FILE}")
"""
    with pytest.raises(SyntaxError):
        create_pybuild(file)
    cleanup_tmp()


def test_stdout():
    """Tests that we can receive stdout from binary executables"""
    file = """
import os
import sys
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_prepare(self):
        output = self.execute("python --version", pipe_output=True)
        if not output.startswith("Python "):
            raise Exception("Incorrect output " + output)
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    cleanup_tmp()


def test_git():
    """Tests that we can execute the git executable within the sandbox"""
    file = """
import os
import sys
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        self.execute("git --version")

    def src_prepare(self):
        self.execute("git --version")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    src_unpack(mod, env.TMP_DIR)
    cleanup_tmp()


def test_perl():
    """Tests that we can execute the perl executable within the sandbox"""
    if not shutil.which("perl"):
        pytest.skip("Perl not installed")

    file = """
import os
import sys
from pybuild import Pybuild1

class Mod(Pybuild1):
    NAME="Test"
    DESC="Test"
    LICENSE="GPL-3"

    def src_unpack(self):
        self.execute("perl --version")

    def src_prepare(self):
        self.execute("perl --version")
"""
    create_pybuild(file)
    mod = __load_file(TMP_FILE)
    src_prepare(mod, env.TMP_DIR)
    src_unpack(mod, env.TMP_DIR)
    cleanup_tmp()
