from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFBibliographyAT.interface import IBibliographicItem
from Products.CMFBibliographyAT.interface import IBibliographyFolder
from Products.CMFBibliographyAT.interface import ILargeBibliographyFolder


class CiteprocSetupViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('citeproc_setup.pt')

    def available(self):
        if (IBibliographicItem.providedBy(self.context) or
            IBibliographyFolder.providedBy(self.context) or
            ILargeBibliographyFolder.providedBy(self.context)):
            return True
        return False