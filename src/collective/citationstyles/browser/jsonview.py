
import json
from zope.component import queryUtility, getMultiAdapter
from zope.publisher.browser import BrowserView

from collective.citationstyles.interfaces import ICitationIterator
from collective.citationstyles.interfaces import ICitationRenderer


class CitationJSONView(BrowserView):
    """uses a utility to render the context as json
    """

    def __call__(self):
        self._setHeader()
        items = getMultiAdapter((self.context, self.request), ICitationIterator)
        renderer = queryUtility(ICitationRenderer, default=None)
        result = {}
        if renderer:
            for item in items:
                rendered = renderer(item)
                result[rendered['id']] = rendered
        try:
            json_reply = json.dumps(result)
            return json_reply
        except TypeError, e:
            reply = {'error': str(e)}
            return json.dumps(reply)

    def _setHeader(self):
        self.request.RESPONSE.setHeader('content-type',
                                        "application/json; charset='utf-8'")
