from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFBibliographyAT.interface import IBibliographicItem


class CiteprocSetupViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('citeproc_setup.pt')

    def available(self):
        import pdb; pdb.set_trace( )
        return IBibliographicItem.providedBy(self.context)