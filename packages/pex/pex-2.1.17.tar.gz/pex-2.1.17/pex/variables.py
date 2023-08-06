# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

# Due to the PEX_ properties, disable checkstyle.
# checkstyle: noqa

from __future__ import absolute_import

import os
import sys
from contextlib import contextmanager

from pex import pex_warnings
from pex.common import can_write_dir, die, safe_mkdtemp
from pex.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Iterator, Optional, Tuple, TypeVar

    _T = TypeVar("_T", str, int, bool)

__all__ = ("ENV", "Variables")


class Variables(object):
    """Environment variables supported by the PEX runtime."""

    @classmethod
    def process_pydoc(cls, pydoc):
        # type: (Optional[str]) -> Tuple[str, str]
        if pydoc is None:
            return "Unknown", "Unknown"
        pydoc_lines = pydoc.splitlines()
        variable_type = pydoc_lines[0]
        variable_text = " ".join(filter(None, (line.strip() for line in pydoc_lines[2:])))
        return variable_type, variable_text

    @classmethod
    def iter_help(cls):
        # type: () -> Iterator[Tuple[str, str, str]]
        for variable_name, value in sorted(cls.__dict__.items()):
            if not variable_name.startswith("PEX_"):
                continue
            variable_type, variable_text = cls.process_pydoc(getattr(value, "__doc__"))
            yield variable_name, variable_type, variable_text

    @classmethod
    def from_rc(cls, rc=None):
        # type: (Optional[str]) -> Dict[str, str]
        """Read pex runtime configuration variables from a pexrc file.

        :param rc: an absolute path to a pexrc file.
        :return: A dict of key value pairs found in processed pexrc files.
        """
        ret_vars = {}  # type: Dict[str, str]
        rc_locations = [
            "/etc/pexrc",
            "~/.pexrc",
            os.path.join(os.path.dirname(sys.argv[0]), ".pexrc"),
        ]
        if rc:
            rc_locations.append(rc)
        for filename in rc_locations:
            try:
                with open(os.path.expanduser(filename)) as fh:
                    rc_items = map(cls._get_kv, fh)
                    ret_vars.update(dict(filter(None, rc_items)))
            except IOError:
                continue
        return ret_vars

    @classmethod
    def _get_kv(cls, variable):
        kv = variable.strip().split("=")
        if len(list(filter(None, kv))) == 2:
            return kv

    def __init__(self, environ=None, rc=None, use_defaults=True):
        # type: (Optional[Dict[str, str]], Optional[str], bool) -> None
        self._use_defaults = use_defaults
        self._environ = environ.copy() if environ is not None else os.environ.copy()
        if not self.PEX_IGNORE_RCFILES:
            rc_values = self.from_rc(rc).copy()
            rc_values.update(self._environ)
            self._environ = rc_values

    def copy(self):
        # type: () -> Dict[str, str]
        return self._environ.copy()

    def _defaulted(self, default):
        # type: (Optional[_T]) -> Optional[_T]
        return default if self._use_defaults else None

    def _get_bool(self, variable, default=False):
        # type: (str, Optional[bool]) -> Optional[bool]
        value = self._environ.get(variable)
        if value is None:
            return self._defaulted(default)
        if value.lower() in ("0", "false"):
            return False
        if value.lower() in ("1", "true"):
            return True
        die("Invalid value for %s, must be 0/1/false/true, got %r" % (variable, value))

    def _get_string(self, variable, default=None):
        # type: (str, Optional[str]) -> Optional[str]
        return self._environ.get(variable, self._defaulted(default))

    def _get_path(self, variable, default=None):
        # type: (str, Optional[str]) -> Optional[str]
        value = self._get_string(variable, default=default)
        if value is not None:
            value = os.path.realpath(os.path.expanduser(value))
        return value

    def _get_int(self, variable, default=None):
        # type: (str, Optional[int]) -> Optional[int]
        try:
            return int(self._environ[variable])
        except ValueError:
            die(
                "Invalid value for %s, must be an integer, got %r"
                % (variable, self._environ[variable])
            )
        except KeyError:
            return self._defaulted(default)

    def strip(self):
        # type: () -> Variables
        stripped_environ = {
            k: v for k, v in self.copy().items() if not k.startswith(("PEX_", "__PEX_"))
        }
        return Variables(environ=stripped_environ)

    def strip_defaults(self):
        # type: () -> Variables
        """Returns a copy of these variables but with defaults stripped.

        Any variables not explicitly set in the environment will have a value of `None`.
        """
        return Variables(environ=self.copy(), use_defaults=False)

    @contextmanager
    def patch(self, **kw):
        # type: (**str) -> Iterator[Dict[str, str]]
        """Update the environment for the duration of a context."""
        old_environ = self._environ
        self._environ = self._environ.copy()
        self._environ.update(kw)
        yield self._environ
        self._environ = old_environ

    @property
    def PEX_ALWAYS_CACHE(self):
        # type: () -> Optional[bool]
        """Boolean.

        Always write PEX dependencies to disk prior to invoking regardless whether or not the
        dependencies are zip-safe.  For certain dependencies that are very large such as numpy, this
        can reduce the RAM necessary to launch the PEX.  The data will be written into $PEX_ROOT,
        which by default is $HOME/.pex.  Default: false.
        """
        return self._get_bool("PEX_ALWAYS_CACHE", default=False)

    @property
    def PEX_COVERAGE(self):
        # type: () -> Optional[bool]
        """Boolean.

        Enable coverage reporting for this PEX file.  This requires that the "coverage" module is
        available in the PEX environment.  Default: false.
        """
        return self._get_bool("PEX_COVERAGE", default=False)

    @property
    def PEX_COVERAGE_FILENAME(self):
        # type: () -> Optional[str]
        """Filename.

        Write the coverage data to the specified filename.  If PEX_COVERAGE_FILENAME is not
        specified but PEX_COVERAGE is, coverage information will be printed to stdout and not saved.
        """
        return self._get_path("PEX_COVERAGE_FILENAME", default=None)

    @property
    def PEX_FORCE_LOCAL(self):
        # type: () -> Optional[bool]
        """Boolean.

        Force this PEX to be not-zip-safe. This forces all code and dependencies to be written into
        $PEX_ROOT prior to invocation.  This is an option for applications with static assets that
        refer to paths relative to __file__ instead of using pkgutil/pkg_resources.  Also see
        PEX_UNZIP which will cause the complete PEX file to be unzipped and re-executed which can
        often improve startup latency in addition to providing support for __file__ access.
        Default: false.
        """
        return self._get_bool("PEX_FORCE_LOCAL", default=False)

    @property
    def PEX_UNZIP(self):
        # type: () -> Optional[bool]
        """Boolean.

        Force this PEX to unzip itself to $PEX_ROOT and re-execute from there.  If the pex file will
        be run multiple times under a stable $PEX_ROOT the unzipping will only be performed once and
        subsequent runs will enjoy lower startup latency.  Default: false.
        """
        return self._get_bool("PEX_UNZIP", default=False)

    @property
    def PEX_IGNORE_ERRORS(self):
        # type: () -> Optional[bool]
        """Boolean.

        Ignore any errors resolving dependencies when invoking the PEX file. This can be useful if
        you know that a particular failing dependency is not necessary to run the application.
        Default: false.
        """
        return self._get_bool("PEX_IGNORE_ERRORS", default=False)

    @property
    def PEX_INHERIT_PATH(self):
        # type: () -> Optional[str]
        """String (false|prefer|fallback)

        Allow inheriting packages from site-packages, user site-packages and the PYTHONPATH. By default,
        PEX scrubs any non stdlib packages from sys.path prior to invoking the application. Using
        'prefer' causes PEX to shift any non-stdlib packages before the pex environment on sys.path and
        using 'fallback' shifts them after instead.

        Using this option is generally not advised, but can help in situations when certain dependencies
        do not conform to standard packaging practices and thus cannot be bundled into PEX files.

        See also PEX_EXTRA_SYS_PATH for how to *add* to the sys.path.

        Default: false.
        """
        return self._get_string("PEX_INHERIT_PATH", default="false")

    @property
    def PEX_INTERPRETER(self):
        # type: () -> Optional[bool]
        """Boolean.

        Drop into a REPL instead of invoking the predefined entry point of this PEX. This can be
        useful for inspecting the PEX environment interactively.  It can also be used to treat the PEX
        file as an interpreter in order to execute other scripts in the context of the PEX file, e.g.
        "PEX_INTERPRETER=1 ./app.pex my_script.py".  Equivalent to setting PEX_MODULE to empty.
        Default: false.
        """
        return self._get_bool("PEX_INTERPRETER", default=False)

    @property
    def PEX_MODULE(self):
        # type: () -> Optional[str]
        """String.

        Override the entry point into the PEX file.  Can either be a module, e.g.
        'SimpleHTTPServer', or a specific entry point in module:symbol form, e.g.  "myapp.bin:main".
        """
        return self._get_string("PEX_MODULE", default=None)

    @property
    def PEX_PROFILE(self):
        # type: () -> Optional[bool]
        """Boolean.

        Enable application profiling.  If specified and PEX_PROFILE_FILENAME is not specified, PEX
        will print profiling information to stdout.
        """
        return self._get_bool("PEX_PROFILE", default=False)

    @property
    def PEX_PROFILE_FILENAME(self):
        # type: () -> Optional[str]
        """Filename.

        Profile the application and dump a profile into the specified filename in the standard
        "profile" module format.
        """
        return self._get_path("PEX_PROFILE_FILENAME", default=None)

    @property
    def PEX_PROFILE_SORT(self):
        # type: () -> Optional[str]
        """String.

        Toggle the profile sorting algorithm used to print out profile columns.  Default:
        'cumulative'.
        """
        return self._get_string("PEX_PROFILE_SORT", default="cumulative")

    @property
    def PEX_PYTHON(self):
        # type: () -> Optional[str]
        """String.

        Override the Python interpreter used to invoke this PEX.  Can be either an absolute path to
        an interpreter or a base name e.g.  "python3.3".  If a base name is provided, the $PATH will
        be searched for an appropriate match.
        """
        return self._get_string("PEX_PYTHON", default=None)

    @property
    def PEX_PYTHON_PATH(self):
        # type: () -> Optional[str]
        """String.

        A colon-separated string containing paths of blessed Python interpreters
        for overriding the Python interpreter used to invoke this PEX. Can be absolute paths to
        interpreters or standard $PATH style directory entries that are searched for child files that
        are python binaries.

        Ex: "/path/to/python27:/path/to/python36-distribution/bin"
        """
        return self._get_string("PEX_PYTHON_PATH", default=None)

    @property
    def PEX_EXTRA_SYS_PATH(self):
        # type: () -> Optional[str]
        """String.

        A colon-separated string containing paths to add to the runtime sys.path.

        Should be used sparingly, e.g., if you know that code inside this PEX needs to
        interact with code outside it.

        Ex: "/path/to/lib1:/path/to/lib2"

        This is distinct from PEX_INHERIT_PATH, which controls how the interpreter's
        existing sys.path (which you may not have control over) is scrubbed.

        See also PEX_PATH for how to merge packages from other pexes into the current environment.
        """
        return self._get_string("PEX_EXTRA_SYS_PATH", default=None)

    @property
    def PEX_ROOT(self):
        # type: () -> Optional[str]
        """Directory.

        The directory location for PEX to cache any dependencies and code.  PEX must write not-zip-
        safe eggs and all wheels to disk in order to activate them.  Default: ~/.pex
        """
        pex_root = self._get_path("PEX_ROOT", default=os.path.expanduser("~/.pex"))

        if pex_root is None:
            # PEX_ROOT is not set and we're running in stripped_defaults mode.
            return None

        if not can_write_dir(pex_root):
            tmp_root = os.path.realpath(safe_mkdtemp())
            pex_warnings.warn(
                "PEX_ROOT is configured as {pex_root} but that path is un-writeable, "
                "falling back to a temporary PEX_ROOT of {tmp_root} which will hurt "
                "performance.".format(pex_root=pex_root, tmp_root=tmp_root)
            )
            pex_root = self._environ["PEX_ROOT"] = tmp_root

        return pex_root

    @property
    def PEX_PATH(self):
        # type: () -> Optional[str]
        """A set of one or more PEX files.

        Merge the packages from other PEX files into the current environment.  This allows you to
        do things such as create a PEX file containing the "coverage" module or create PEX files
        containing plugin entry points to be consumed by a main application.  Paths should be
        specified in the same manner as $PATH, e.g. PEX_PATH=/path/to/pex1.pex:/path/to/pex2.pex
        and so forth.

        See also PEX_EXTRA_SYS_PATH for how to add arbitrary entries to the sys.path.
        """
        return self._get_string("PEX_PATH", default="")

    @property
    def PEX_SCRIPT(self):
        # type: () -> Optional[str]
        """String.

        The script name within the PEX environment to execute.  This must either be an entry point
        as defined in a distribution's console_scripts, or a script as defined in a distribution's
        scripts section.  While Python supports any script including shell scripts, PEX only
        supports invocation of Python scripts in this fashion.
        """
        return self._get_string("PEX_SCRIPT", default=None)

    @property
    def PEX_TEARDOWN_VERBOSE(self):
        # type: () -> Optional[bool]
        """Boolean.

        Enable verbosity for when the interpreter shuts down.  This is mostly only useful for
        debugging PEX itself.  Default: false.
        """
        return self._get_bool("PEX_TEARDOWN_VERBOSE", default=False)

    @property
    def PEX_VERBOSE(self):
        # type: () -> Optional[int]
        """Integer.

        Set the verbosity level of PEX debug logging.  The higher the number, the more logging, with
        0 being disabled.  This environment variable can be extremely useful in debugging PEX
        environment issues.  Default: 0
        """
        return self._get_int("PEX_VERBOSE", default=0)

    @property
    def PEX_IGNORE_RCFILES(self):
        # type: () -> Optional[bool]
        """Boolean.

        Explicitly disable the reading/parsing of pexrc files (~/.pexrc). Default: false.
        """
        return self._get_bool("PEX_IGNORE_RCFILES", default=False)

    @property
    def PEX_EMIT_WARNINGS(self):
        # type: () -> Optional[bool]
        """Boolean.

        Emit UserWarnings to stderr. When false, warnings will only be logged at PEX_VERBOSE >= 1.
        When unset the build-time value of `--emit-warnings` will be used. Default: unset.
        """
        return self._get_bool("PEX_EMIT_WARNINGS", default=None)

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self._environ)


# Global singleton environment
ENV = Variables()
