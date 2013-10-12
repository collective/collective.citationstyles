
import json
from zope.component import queryUtility
from zope.component import queryMultiAdapter
from zope.publisher.browser import BrowserView

from collective.citationstyles.interfaces import ICitationIterator
from collective.citationstyles.interfaces import ICitationRenderer


class CitationJSONView(BrowserView):
    """uses a utility to render the context as json
    """

    def __call__(self):
        self._setHeader()
        error = {'error': 1}
        items = queryMultiAdapter(
            (self.context, self.request), ICitationIterator
        )
        if items is None:
            error['error'] = 'not a citation context'
            reply = error
        else:
            renderer = queryUtility(ICitationRenderer, default=None)
            result = {}
            if not renderer:
                error['error'] = 'citation renderer not available'
                reply = error
            else:
                for item in items:
                    rendered = renderer(item)
                    result[rendered['id']] = rendered
            try:
                json_reply = json.dumps(result)
                return json_reply
            except TypeError, e:
                error['error'] = str(e)
                reply = error

        return json.dumps(reply)

    def _setHeader(self):
        self.request.RESPONSE.setHeader('content-type',
                                        "application/json; charset='utf-8'")
