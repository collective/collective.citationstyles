import os.path

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID

from plone.testing import z2

from zope.configuration import xmlconfig


BIBTEX_TEST_BIB = os.path.join(os.path.dirname(__file__), 'tests/source.bib')


class CollectivecitationstylesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.citationstyles
        xmlconfig.file(
            'configure.zcml',
            collective.citationstyles,
            context=configurationContext
        )
        import Products.ATExtensions
        xmlconfig.file(
            'configure.zcml',
            Products.ATExtensions,
            context=configurationContext
        )

        z2.installProduct(app, 'Products.CMFBibliographyAT')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.CMFBibliographyAT')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.citationstyles:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        self.createBibFolder(portal)
        self.createOldStyleCollection(portal)
        self.createNewStyleCollection(portal)
        setRoles(portal, TEST_USER_ID, ['Member'])
        logout()

    def createBibFolder(self, portal):
        bf_id = portal.invokeFactory("BibliographyFolder", id="bib_folder")
        bib_folder = portal[bf_id]
        bib_source = open(BIBTEX_TEST_BIB, 'r').read()
        bib_folder.processImport(bib_source, 'source.bib')

    def createOldStyleCollection(self, portal):
        if not 'Topic' in portal.portal_types:
            return
        if not portal.portal_types.Topic.global_allow:
            portal.portal_types.Topic.global_allow = True
        topic_id = "topic"
        portal.invokeFactory('Topic', topic_id)
        topic = portal[topic_id]
        crit = topic.addCriterion('portal_type', 'ATSimpleStringCriterion')
        crit.setValue('BibliographyFolder')

    def createNewStyleCollection(self, portal):
        collection_id = "collection"
        portal.invokeFactory('Collection', collection_id)
        collection = portal[collection_id]
        query = [{
            'i': 'portal_type',
            'o': 'plone.app.querystring.operation.string.is',
            'v': 'BibliographyFolder',
        }]
        collection.setQuery(query)


COLLECTIVE_CITATIONSTYLES_FIXTURE = CollectivecitationstylesLayer()
COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CITATIONSTYLES_FIXTURE,),
    name="CollectivecitationstylesLayer:Integration"
)
COLLECTIVE_CITATIONSTYLES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CITATIONSTYLES_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectivecitationstylesLayer:Functional"
)
