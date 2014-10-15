from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class TestFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import xsgs.policy
        xmlconfig.file('configure.zcml', xsgs.policy, context=configurationContext)
    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'xsgs.policy:default')

FIXTURE = TestFixture()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name="TestFixture:Integration")
FUNCTION_TESTING = FunctionalTesting(bases=(FIXTURE,), name="TestFixture:Functional")
