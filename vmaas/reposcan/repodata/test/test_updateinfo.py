"""
Unit test classes for updateinfo module.
"""
import unittest
from xml.etree.ElementTree import ParseError
from vmaas.reposcan.repodata.updateinfo import UpdateInfoMD

KNOWN_UPDATE_TYPES = ["security", "bugfix", "enhancement", "newpackage"]


class TestUpdateInfoMD(unittest.TestCase):
    """Test UpdateInfoMD class."""
    def setUp(self):
        """Setup example updateinfo file."""
        self.updateinfo = UpdateInfoMD("test_data/repodata/updateinfo.xml")

    def _test_reference(self, reference):
        intended_fields = ["href", "id", "type", "title"]
        actual_fields = reference.keys()
        for field in intended_fields:
            self.assertTrue(field in actual_fields)
        for field in actual_fields:
            self.assertTrue(field in intended_fields)

    def _test_pkg_ref(self, pkg_ref):
        intended_fields = ["name", "epoch", "ver", "rel", "arch"]
        actual_fields = pkg_ref.keys()
        for field in intended_fields:
            self.assertTrue(field in actual_fields)
        for field in actual_fields:
            self.assertTrue(field in intended_fields)

    def _test_update(self, update):
        intended_fields = ["from", "status", "type", "version", "id", "title", "issued", "rights", "release",
                           "summary", "description", "references", "pkglist", "updated", "severity", "solution",
                           "reboot"]
        actual_fields = update.keys()
        for field in intended_fields:
            self.assertTrue(field in actual_fields, field)
        for field in actual_fields:
            self.assertTrue(field in intended_fields, field)

        self.assertIsInstance(update["references"], list)
        self.assertIsInstance(update["pkglist"], list)

        for reference in update["references"]:
            self._test_reference(reference)

        for pkg_ref in update["pkglist"]:
            self._test_pkg_ref(pkg_ref)

        self._test_reboot(update)

        # Check known update types
        self.assertTrue(update["type"] in KNOWN_UPDATE_TYPES)

    def _test_reboot(self, update: dict):
        """Check that advisories with <reboot_suggested> tag were parsed correctly"""
        self.assertIsInstance(update['reboot'], bool)
        if update['id'] in ['FEDORA-2017-63f9b40927', 'FEDORA-2017-14fbbab6e0', 'FEDORA-2017-82315d72d0']:
            self.assertTrue(update['reboot'], '%s - reboot' % update['id'])
        else:
            self.assertFalse(update['reboot'], '%s - reboot' % update['id'])

    def test_invalid_file(self):
        """Test case when file doesn't exist or is invalid."""
        with self.assertRaises(FileNotFoundError):
            UpdateInfoMD("/file/does/not/exist")
        with self.assertRaises(ParseError):
            UpdateInfoMD("/dev/null")

    def test_updates(self):
        """Test parsed updates metadata fields and counts."""
        updates = self.updateinfo.list_updates()
        # Test fields of updates in list
        for update in updates:
            self._test_update(update)
