import unittest2 as unittest
import json

from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID

from collective.citationstyles.browser.json import CitationJSONView
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
            self.assertTrue(expected in actual)

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
            self.assertTrue(ctxt.UID() in actual)

    # XXX: This is needed, but we are skipping it for now because of the 
    # old/new collections mess across Plone 4 versions
    # 
    # def testViewAvailableOnCollections(self):
    #     ctxt = self._createCollection()
    #     view = self.getView(ctxt)
    #     self.assertTrue(view is not None)
    #     self.assertTrue(isinstance(view, CitationJSONView))

    
