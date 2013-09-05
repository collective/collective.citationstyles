from Acquisition import aq_base

from zope.component import queryAdapter

from bibliograph.core.interfaces import IBibliographicReference
from Products.CMFBibliographyAT.interface import IBibliographicItem


class BibliograpyIterator(object):

    def __init__(self, context):
        self.context = context

    def __iter__(self):
        checkme = aq_base(self.context)
        if IBibliographicItem.providedBy(checkme):
            biblio = queryAdapter(self.context, IBibliographicReference)
            if biblio is not None:
                yield biblio
        # common collection/topic API
        elif hasattr(checkme, 'queryCatalog'):
            for brain in self.context.queryCatalog():
                obj = brain.getObject()
                biblio = queryAdapter(obj, IBibliographicReference)
                if biblio is not None:
                    yield biblio
        # folderish thingies
        elif hasattr(checkme, 'objectValues'):
            for obj in self.context.objectValues():
                if IBibliographicItem.providedBy(obj):
                    biblio = queryAdapter(obj, IBibliographicReference)
                    if biblio is not None:
                        yield biblio
