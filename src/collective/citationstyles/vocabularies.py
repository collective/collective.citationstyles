from zope.interface import implements
from zope.component import getUtility

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry

from collective.citationstyles.interfaces import ISettings
from collective.citationstyles import citationstylesMessageFactory as _

class SelectableStylesheetsVocabulary(object):
    """List of stylesheets that can be selected for content.

       Includes an option to use the default (and the current default is shown).
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)

        default_label = '%s (%s)' % (_(u'Site default'), settings.default_style)
        terms.append(SimpleVocabulary.createTerm('', '', default_label))

        citation_styles = settings.citation_styles
        for style in citation_styles.keys():
            token_val = style
            if isinstance(token_val, unicode):
                # escape unicode so that the token rendered in the form is
                # guaranteed to be only 7 bits
                token_val = style.encode('unicode_escape')
            terms.append(SimpleVocabulary.createTerm(style, token_val, style))
        return SimpleVocabulary(terms)

SelectableStylesheetsVocabularyFactory = SelectableStylesheetsVocabulary()
