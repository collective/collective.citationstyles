from Acquisition import aq_base

from zope.component import queryAdapter

from bibliograph.core.interfaces import IBibliographicReference
from Products.CMFBibliographyAT.interface import IBibliographicItem

import logging
logger = logging.getLogger('collective.citationstyles')


class BaseBibliographyIterator(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __iter__(self):
        for item in self._get_items():
            try:
                biblio = queryAdapter(item, IBibliographicReference)
            except AttributeError, e:
                # this can happen if a bibliographic item does
                # not have one of the required attributes for the 
                # adapter.  Log the error
                msg = "Adaptation of {} to IBibliographicReference "
                msg += "failed due to a missing attribute: {}"
                logger.warn(msg.format(item.id, str(e)))
                continue
            if biblio is not None:
                yield biblio

    def _get_items(self):
        """subclasses must implement this method"""
        raise NotImplementedError



class NaiveBibliograpyIterator(object):
    """simple implementation that does not support pagination properly
    """

    def _get_items(self):
        checkme = aq_base(self.context)
        if IBibliographicItem.providedBy(checkme):
            yield self.context
        # common collection/topic API
        elif hasattr(checkme, 'queryCatalog'):
            for brain in self.context.queryCatalog():
                obj = brain.getObject()
                yield obj
        # simple folderish thingies
        elif hasattr(checkme, 'objectValues'):
            for obj in self.context.objectValues():
                yield obj
