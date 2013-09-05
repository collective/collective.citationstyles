VALID_CSL_VARIABLES = [
    'abstract', 'annote', 'archive', 'archive_location', 'archive-place',
    'authority', 'call-number', 'chapter-number', 'citation-label',
    'citation-number', 'collection-title', 'container-title', 'DOI',
    'edition', 'event', 'event-place', 'first-reference-note-number',
    'genre', 'ISBN', 'issue', 'jurisdiction', 'keyword', 'locator',
    'medium', 'note', 'number', 'number-of-pages', 'number-of-volumes',
    'original-publisher', 'original-publisher-place', 'original-title',
    'page', 'page-first', 'publisher', 'publisher-place', 'references',
    'section', 'status', 'title', 'URL', 'version', 'volume',
    'year-suffix', 'accessed', 'container', 'event-date', 'issued',
    'original-date', 'author', 'editor', 'translator', 'recipient',
    'interviewer', 'publisher', 'composer', 'original-publisher',
    'original-author', 'container-author', 'collection-editor',
]

class ReferenceCSLRenderer(object):
    """convert IBibliographicReference items to python dict
    
    The keys and structure of the dict must match valid 'variables' for
    CSL1.0 (http://citationstyles.org/downloads/specification-csl10-20100530.html#appendix-i-variables)
    
    The dictionaries will be rendered to JSON and so must contain only python
    primitives.
    """

    def __call__(self, bib_ref):
        output = {}
        output['id'] = bib_ref.context.UID()
        # transfer any keys in '__dict__' that are already valid csl variables
        for key in bib_ref.__dict__:
            if key in VALID_CSL_VARIABLES:
                val = getattr(bib_ref, key, None)
                if val:
                    output[key] = val
        return output

    def handle_publication_dates(self, bib_ref):
        dates = {}
        return dates