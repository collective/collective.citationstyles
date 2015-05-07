from zope.interface import Interface
from zope import schema
from collective.citationstyles import citationstylesMessageFactory as _
from collective.citationstyles import DEFAULT_CSL


class ISettings(Interface):
    citation_styles = schema.Dict(title=_(u'Citation Styles'),
        description=_(u'Specify name/content pairs for citation styles'),
        key_type=schema.TextLine(),
        value_type=schema.Text(),
        default=None)

    default_style = schema.TextLine(title=_(u'Default Style'),
        description=_(u'The default citation style to use on the site'),
        default=DEFAULT_CSL)


class ICitationRenderer(Interface):
    """utility renders"""


class ICitationIterator(Interface):
    """adapter that produces an iterable of IBibliographicReference items"""


class ICitationStylesLayer(Interface):
    """browser layer interface"""


class IBibViewMarker(Interface):
    """A marker interfaces for views which potentially contain
    bibliographic items"""
