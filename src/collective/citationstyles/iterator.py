from zope.component import queryAdapter

from bibliograph.core.interfaces import IBibliographicReference
from Products.CMFBibliographyAT.interface import IBibliographicItem


class BibliograpyIterator(object):

    def __init__(self, context):
        self.context = context

    def __iter__(self):
        if IBibliographicItem.providedBy(self.context):
            biblio = queryAdapter(self.context, IBibliographicReference)
            if biblio is not None:
                yield biblio
        elif hasattr(self.context, 'objectValues'):
            for obj in self.context.objectValues():
                if IBibliographicItem.providedBy(obj):
                    biblio = queryAdapter(obj, IBibliographicReference)
                    if biblio is not None:
                        yield biblio
