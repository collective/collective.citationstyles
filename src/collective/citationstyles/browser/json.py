from zope.publisher.browser import BrowserView


class CitationJSONView(BrowserView):
    """uses a utility to render the context as json
    """
    # items = ICitationIterator(self.context)
    # renderer = queryUtility(ICitationRenderer, default=None)
    # result = {}
    # if renderer:
    #     for item in itmes:
    #         rendered = renderer(item)
    #         result[rendered['id']] = rendered
    # return json.dumps(result)
