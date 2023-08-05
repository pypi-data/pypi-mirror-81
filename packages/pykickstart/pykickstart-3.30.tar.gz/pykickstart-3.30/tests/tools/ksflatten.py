import os
import sys
try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO
from tools import ksflatten
from pykickstart import __version__
import unittest.mock as mock
from unittest import TestCase
from unittest import skipUnless
from contextlib import contextmanager
from tests.tools.utils import mktempfile


@contextmanager
def capture(command, *args, **kwargs):
    stdout, sys.stdout = sys.stdout, StringIO()
    stderr, sys.stderr = sys.stderr, StringIO()
    try:
        retval = command(*args, **kwargs)
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        yield (retval, sys.stdout.read(), sys.stderr.read())
    finally:
        sys.stdout = stdout
        sys.stderr = stderr


class NoConfigSpecified_TestCase(TestCase):
    @mock.patch('sys.exit', create=True)
    def runTest(self, _exit):
        with capture(ksflatten.main, []) as output:
            retval, msg = output[0] 
            self.assertEqual(retval, 1)
            self.assertEqual(msg, 'Need to specify a config to flatten')

class WrongKSPath_TestCase(TestCase):
    def runTest(self):
        retval, msg = ksflatten.main(['--version', 'F26', '--config', '/non/existing'])
        self.assertEqual(retval, 1)
        self.assertTrue(msg.find('Failed to parse kickstart file') > -1)

class ReadKickstartIOError_TestCase(TestCase):
    @mock.patch('pykickstart.parser.KickstartParser.readKickstart')
    def runTest(self, _readKickstart):
        _readKickstart.side_effect = IOError
        retval, msg = ksflatten.main(['--version', 'F26', '--config', '/dev/null'])
        self.assertEqual(retval, 1)
        self.assertTrue(msg.find('Failed to read kickstart file') > -1)

class ValidKSFile_ToStdOut_TestCase(TestCase):
    def setUp(self):
        self._include_path = mktempfile("text", prefix="ks-include")
        ks_content = "autopart\n%%include %s" % self._include_path
        self._ks_path = mktempfile(ks_content)

    def tearDown(self):
        os.unlink(self._ks_path)
        os.unlink(self._include_path)

    def runTest(self):
        with capture(ksflatten.main, ['--version', 'F26', '--config', self._ks_path]) as output:
            self.assertEqual(output[1], "# Generated by pykickstart v%s\n#version=F26\n# Use text mode install\ntext\n\n# System bootloader configuration\nbootloader --location=none\nautopart\n" % __version__)

class ValidKSFile_TestCase(TestCase):
    def setUp(self):
        self._include_path = mktempfile("text", prefix="ks-include")
        ks_content = "autopart\n%%include %s" % self._include_path
        self._ks_path = mktempfile(ks_content)
        self._output_path = mktempfile()

    def tearDown(self):
        os.unlink(self._ks_path)
        os.unlink(self._include_path)
        os.unlink(self._output_path)

    def runTest(self):
        retval, msg = ksflatten.main(['--version', 'F26',
                                      '--config', self._ks_path,
                                      '--output', self._output_path])
        self.assertEqual(retval, 0)
        self.assertEqual(msg, "")
        f = open(self._output_path, 'r')
        output = f.read()
        f.close()
        self.assertEqual(output, "# Generated by pykickstart v%s\n#version=F26\n# Use text mode install\ntext\n\n# System bootloader configuration\nbootloader --location=none\nautopart\n" % __version__)

@skipUnless(os.getuid(), "test requires non-root access")
class FailsToOpenOutputFile_TestCase(TestCase):
    def setUp(self):
        self._include_path = mktempfile("text", prefix="ks-include")
        ks_content = "autopart\n%%include %s" % self._include_path
        self._ks_path = mktempfile(ks_content)

        self._output_path = mktempfile()
        # create IOError
        os.chmod(self._output_path, 0o000)

    def tearDown(self):
        os.unlink(self._ks_path)
        os.unlink(self._include_path)
        os.unlink(self._output_path)

    def runTest(self):
        retval, msg = ksflatten.main(['--version', 'F26',
                                      '--config', self._ks_path,
                                      '--output', self._output_path])
        self.assertEqual(retval, 1)
        self.assertTrue(msg.find('Failed to open output file') > -1)
