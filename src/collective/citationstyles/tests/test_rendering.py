import unittest2 as unittest

from collective.citationstyles.testing import \
    COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING


class TestRendering(unittest.TestCase):

    layer = COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']


