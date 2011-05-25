# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from eke.knowledge.testing import EKE_KNOWLEDGE_FIXTURE
from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting
from plone.testing import z2

class EKESite(PloneSandboxLayer):
    defaultBases = (EKE_KNOWLEDGE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import eke.site
        self.loadZCML(package=eke.site)
        z2.installProduct(app, 'eke.site')
        import eke.site.tests.base
        eke.site.tests.base.registerLocalTestData()
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'eke.site:default')
    def teatDownZope(self, app):
        z2.uninstallProduct(app, 'eke.site')

EKE_SITE_FIXTURE = EKESite()
EKE_SITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EKE_SITE_FIXTURE,),
    name='EKESite:Integration',
)
EKE_SITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EKE_SITE_FIXTURE,),
    name='EKESite:Functional',
)
