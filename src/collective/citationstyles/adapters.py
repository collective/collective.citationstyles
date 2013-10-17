from Acquisition import aq_base

from zope.component import queryAdapter

from bibliograph.core.interfaces import IBibliographicReference
from Products.CMFBibliographyAT.interface import IBibliographicItem

import logging
logger = logging.getLogger('collective.citationstyles')


class BibliographyIterator(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

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
                    try:
                        biblio = queryAdapter(obj, IBibliographicReference)
                    except AttributeError, e:
                        # this can happen if a bibliographic item does
                        # not have one of the required attributes for the 
                        # adapter.  Log the error
                        msg = "Adaptation of {} to IBibliographicReference "
                        msg += "failed due to a missing attribute: {}"
                        logger.warn(msg.format(obj.id, str(e)))
                        continue
                    if biblio is not None:
                        yield biblio
