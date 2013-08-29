from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


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

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.citationstyles:default')

COLLECTIVE_CITATIONSTYLES_FIXTURE = CollectivecitationstylesLayer()
COLLECTIVE_CITATIONSTYLES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CITATIONSTYLES_FIXTURE,),
    name="CollectivecitationstylesLayer:Integration"
)
COLLECTIVE_CITATIONSTYLES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CITATIONSTYLES_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectivecitationstylesLayer:Functional"
)
