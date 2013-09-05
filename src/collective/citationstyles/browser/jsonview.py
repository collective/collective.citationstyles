
import json
from zope.component import queryUtility
from zope.publisher.browser import BrowserView

from collective.citationstyles.interfaces import ICitationIterator
from collective.citationstyles.interfaces import ICitationRenderer


class CitationJSONView(BrowserView):
    """uses a utility to render the context as json
    """

    def __call__(self):
        items = ICitationIterator(self.context)
        renderer = queryUtility(ICitationRenderer, default=None)
        result = {}
        if renderer:
            for item in items:
                rendered = renderer(item)
                result[rendered['id']] = rendered
        return json.dumps(result)