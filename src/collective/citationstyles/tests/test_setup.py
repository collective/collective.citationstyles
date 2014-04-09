from os.path import basename
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
        self.request = self.layer['request']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        self.js_reg = getToolByName(self.portal, 'portal_javascripts')

    def test_product_is_installed(self):
        """The package and dependencies should be installed"""
        pids = ['collective.citationstyles', 'CMFBibliographyAT',
                'ATExtensions']
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        for pid in pids:
            self.assertTrue(pid in installed,
                            'package appears not to have been installed')

    def test_citation_iteration_adapter_registered(self):
        iterator = ICitationIterator(self.portal, self.request)
        self.assertTrue(iterator is not None)

    def test_citation_renderer_utility_registered(self):
        renderer = queryUtility(ICitationRenderer)
        self.assertTrue(renderer is not None)

    def test_resources_available(self):
        expected = ['citeproc.js', 'xmldom.js', 'xmle4x.js']
        base_resourcepath = '++resource++citationstyles.citeprocjs/'
        for filename in expected:
            resource_path = base_resourcepath + filename
            try:
                self.portal.restrictedTraverse(resource_path)
            except AttributeError:
                self.fail("Unable to traverse to %s" % resource_path)
