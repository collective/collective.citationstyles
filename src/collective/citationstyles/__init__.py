from zope.i18nmessageid import MessageFactory


# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

citationstylesMessageFactory = MessageFactory('collective.citationstyles')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


DEFAULT_STYLES = [
    u'Modern Language Association 7th edition',
    u'American Psychological Association 6th edition',
    u'Chicago Manual of Style 16th edition (note)',
]

DEFAULT_CSL = u'Chicago Manual of Style 16th edition (note)'
