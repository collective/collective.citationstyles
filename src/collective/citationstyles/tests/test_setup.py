import unittest2 as unittest

from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName

from collective.citationstyles.testing import \
    COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING
from collective.citationstyles.interfaces import ICitationIterator
from collective.citationstyles.interfaces import ICitationRenderer


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """The package and dependencies should be installed"""
        pids = ['collective.citationstyles', 'CMFBibliographyAT',
                'ATExtensions']
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        for pid in pids:
            self.assertTrue(pid in installed,
                            'package appears not to have been installed')

    def test_citation_iteration_adapter_registered(self):
        iterator = ICitationIterator(self.portal)
        self.assertTrue(iterator is not None)

    def test_citation_renderer_utility_registered(self):
        renderer = queryUtility(ICitationRenderer)
        self.assertTrue(renderer is not None)
