from bibliograph.core.interfaces import IBibliographicReference

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

BIBREF_TO_CSL_MAPPING = {
    'pages': 'page',
    'journal': 'container-title',
    'address': 'publisher-place',
    'isbn': 'ISBN',
    'booktitle': 'container-title',
    'organization': 'authority',
    'school': 'authority',
    'series': 'collection-title',
    'institution': 'authority',
    'chapter': 'chapter-number',
}

# XXX This is the fallback when we can't figure out what a thing is.  Is this
# really the best option?
FALLBACK_CSL_TYPE = 'book'

CSL_TYPES = [
    'article',
    'article-magazine',
    'article-newspaper',
    'article-journal',
    'bill',
    'book',
    'broadcast',
    'chapter',
    'entry',
    'entry-dictionary',
    'entry-encyclopedia',
    'figure',
    'graphic',
    'interview',
    'legislation',
    'legal_case',
    'manuscript',
    'map',
    'motion_picture',
    'musical_score',
    'pamphlet',
    'paper-conference',
    'patent',
    'post',
    'post-weblog',
    'personal_communication',
    'report',
    'review',
    'review-book',
    'song',
    'speech',
    'thesis',
    'treaty',
    'webpage',
]

BIBTYPES_TO_CSLTYPES_MAPPING = {
    'ArticleReference': 'article-journal',
    'BookReference': 'book',
    'BookletReference': 'pamphlet',
    'InbookReference': 'chapter',
    'IncollectionReference': 'entry',
    'InproceedingsReference': 'paper-conference',
    'Manual': 'pamphlet',
    'MastersthesisReference': 'thesis',
    'PhdthesisReference': 'thesis',
    'PreprintReference': 'webpage',
    'ProceedingsReference': 'book',
    'TechreportReference': 'pamphlet',
}


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
        output['type'] = self.handle_publication_type(bib_ref)
        # handle fields defined by the bibref interface attributes
        output.update(self.handle_bibref_interface(bib_ref))
        output.update(self.handle_additional(bib_ref))
        output.update(self.handle_people(bib_ref))
        
        return output

    def _render_base_unit(self, unit):
        val = ''
        # skip binary annotations?
        if not unit.binary:
            # skip non-plain-text annotations?
            if unit.mimetype == "text/plain":
                val = unit.raw
                # encode raw unicode to bytestrings
                if isinstance(val, unicode):
                    val = val.encode(unit.original_encoding)
        return val

    def handle_bibref_interface(self, bib_ref):
        """handle all attributes and methods for IBibliographicReference"""
        output = {}
        # transfer schema names that are already valid CSL variables
        for key in list(IBibliographicReference):
            if key in VALID_CSL_VARIABLES:
                val = getattr(bib_ref, key, None)
                if val:
                    if key == 'annote':
                        # annote holds BaseUnits, which have renderable content
                        val = self._render_base_unit(val)
                    output[key] = val
            elif key in BIBREF_TO_CSL_MAPPING:
                val = getattr(bib_ref, key, None)
                if val:
                    output[BIBREF_TO_CSL_MAPPING[key]] = val
            else:
                # handle non-standard names here?
                if key == 'source_fields':
                    output.update(self.handle_source_fields(bib_ref))
                elif key == 'publication_year':
                    date_parts = self.handle_publication_date(bib_ref)
                    if date_parts is not None:
                        output['issued'] = date_parts
        return output

    def handle_source_fields(self, bib_ref):
        output = {}
        for key, val in bib_ref.source_fields:
            if key == 'editor':
                # we will handle editor under separate cover.
                continue
            if key in VALID_CSL_VARIABLES:
                if val:
                    output[key] = val
            else:
                if key in BIBREF_TO_CSL_MAPPING:
                    output[BIBREF_TO_CSL_MAPPING[key]] = val

        return output

    def handle_publication_date(self, bib_ref):
        """publication date in csl json is:
        
        'issued': {'date-parts': [[year(, month(, day))]]}
        """
        date_parts = []
        year = getattr(bib_ref, 'publication_year', None)
        month = getattr(bib_ref, 'publication_month', None)
        if year and month:
            date_parts.append([year, month])
        elif year:
            date_parts.append([year])
        else:
            # we have neither year nor month, abandon ship
            return

        return {'date-parts': date_parts}

    def handle_publication_type(self, bib_ref):
        """resolve the content type of this bib_ref to the list of CSL types
        
        If 'publication_type' is availabile in source_fields, attempt to match
        it as well
        """
        ptype = bib_ref.context.portal_type
        pubtype = BIBTYPES_TO_CSLTYPES_MAPPING.get(ptype, None)
        alttype = None
        for key, val in bib_ref.source_fields:
            if key in ['publication_type', 'howpublished']:
                if val.lower() in CSL_TYPES:
                    alttype = val
        if alttype is not None:
            pubtype = alttype

        if pubtype is None:
            pubtype = FALLBACK_CSL_TYPE

        return pubtype

    def handle_additional(self, bib_ref):
        """attempt to resolve fields in getAdditional"""
        output = {}
        for mapping in bib_ref.context.getAdditional():
            key = mapping['key']
            value = mapping['value']
            newkey = None
            if key.lower() in VALID_CSL_VARIABLES:
                newkey = key.lower()
            elif key.lower() in BIBREF_TO_CSL_MAPPING:
                newkey = BIBREF_TO_CSL_MAPPING[key.lower()]
            if newkey and value:
                output[newkey] = value
        return output

    def handle_people(self, bib_ref):
        """deal with authors and editors
        
        data output as list of {'family': 'xxx', 'given': 'xxx'} dicts
        """
        key = 'author'
        if bib_ref.editor_flag:
            key = 'editor'
        authors = []
        for author in bib_ref.getAuthors():
            person = {
                'family': author['lastname'],
                'given': '{firstname} {middlename}'.format(**author).strip()
            }
            authors.append(person)
        return {key: authors}
