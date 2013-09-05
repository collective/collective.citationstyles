import unittest2 as unittest
import json

from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from zope.component import provideUtility
from zope.component import queryUtility
from zope.interface import alsoProvides

from collective.citationstyles.interfaces import ICitationRenderer
from collective.citationstyles.browser.jsonview import CitationJSONView
from collective.citationstyles.testing import \
    COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING


class TestJSONView(unittest.TestCase):

    layer = COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.bib_folder = self.portal.bib_folder

    def _createCollection(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        tid = self.portal.invokeFactory('Collection', 'bibtopic')
        topic = self.portal[tid]
        logout()
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        return topic

    def getView(self, ctxt):
        view = None
        try:
            view = ctxt.restrictedTraverse('@@citations-json')
        except AttributeError:
            pass
        return view

    def testViewAvailableOnBibFolder(self):
        ctxt = self.bib_folder
        view = self.getView(ctxt)
        self.assertTrue(view is not None)
        self.assertTrue(isinstance(view, CitationJSONView))

    def testResponseContentTypeIsJson(self):
        ctxt = self.bib_folder
        self.getView(ctxt)()
        content_type = self.layer['request'].response.getHeader('content-type')
        self.assertEqual("application/json; charset='utf-8'", content_type)

    def testViewOnBibFolderReturnsJSON(self):
        ctxt = self.bib_folder
        view = self.getView(ctxt)
        json_val = view()
        self.assertTrue(json_val)
        try:
            actual = json.loads(json_val)
        except Exception:
            self.fail('invalid json: %s' % json_val)
        for obj in ctxt.objectValues():
            expected = obj.UID()
            self.assertTrue(expected in actual, "UID not included in JSON!")

    def testViewAvailableOnBibItems(self):
        for ctxt in self.bib_folder.objectValues():
            view = self.getView(ctxt)
            self.assertTrue(view is not None)
            self.assertTrue(isinstance(view, CitationJSONView))

    def testViewOnBibItemsReturnsJSON(self):
        for ctxt in self.bib_folder.objectValues():
            view = self.getView(ctxt)
            json_val = view()
            self.assertTrue(json_val)
            try:
                actual = json.loads(json_val)
            except Exception:
                self.fail('invalid json: %s' % json_val)
            self.assertTrue(ctxt.UID() in actual, "UID not included in JSON!")

    def testViewAvailableOnCollections(self):
        ctxt = self.portal['collection']
        view = self.getView(ctxt)
        self.assertTrue(view is not None)
        self.assertTrue(isinstance(view, CitationJSONView))

    def testViewAvailableOnTopics(self):
        ctxt = self.portal['topic']
        view = self.getView(ctxt)
        self.assertTrue(view is not None)
        self.assertTrue(isinstance(view, CitationJSONView))


class DumbRenderer(object):
    """ Render the bare minimum about an IBibliographicReference
    """
    def __call__(self, bib_ref):
        return {'id': bib_ref.title}


class TestJSONViewIntegration(unittest.TestCase):

    layer = COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.bib_folder = self.portal.bib_folder
        self.renderer = DumbRenderer()
        self.orig_renderer = queryUtility(ICitationRenderer)
        alsoProvides(self.renderer, ICitationRenderer)
        provideUtility(self.renderer, ICitationRenderer)

    def tearDown(self):
        provideUtility(self.orig_renderer, ICitationRenderer)

    def testViewOnBibFolderReturnsJSON(self):
        ctxt = self.bib_folder
        view = ctxt.restrictedTraverse('@@citations-json')
        json_val = view()
        self.assertTrue(json_val)
        try:
            actual = json.loads(json_val)
        except Exception:
            self.fail('invalid json: %s' % json_val)
        for obj in ctxt.objectValues():
            expected = obj.Title()
            self.assertTrue(expected in actual)
