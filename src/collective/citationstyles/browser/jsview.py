import os
from json import dumps
from zope.component import getUtility, queryMultiAdapter
from zope.publisher.browser import BrowserView

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.log import log
from ..interfaces import ISettings

LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locale')
LOCALES_AVAILABLE = sorted('-'.join(f.split('.')[0].split('-')[1:]) for f in
                           os.listdir(LOCALES_DIR) if
                           f.lower().endswith('.xml'))
LOCALES_AVAILABLE.reverse() # Reverse so that en-US comes before
                            # en-GB, as is proper
DEFAULT_LOCALE = 'en-US'

_base_js_file = open(os.path.join(os.path.dirname(__file__),
                                  'citation_loader.js'))
BASE_JS = _base_js_file.read()
_base_js_file.close()

class CitationStylesJSView(BrowserView):
    """Renders all CSL files as js variable"""

    def _setHeader(self):
        self.request.RESPONSE.setHeader('content-type',
                                      "application/javascript; charset='utf-8'")
    def render_csl(self):
        """Returns JS rendering of CSL files"""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        styles = settings.citation_styles
        output = []
        for name, value in styles.iteritems():
            output.append('collective_csl_info.add_csl({0}, {1});'.format(
                dumps(name), dumps(value)));
        output.append('collective_csl_info.set_default_csl({0});'.format(
            dumps(settings.default_style)))
        return '\n'.join(output)

    def render_locales(self):
        """Returns JS rendering of Locale file(s).  Currently we only
        load the site default locale, and fall back to en-US.
        """
        self._setHeader()
        portal_state = queryMultiAdapter((self.context, self.request),
                                         name=u'plone_portal_state')
        self.portal = portal_state.portal()
        locale = portal_state.default_language()
        # Capialization format en-US
        locale = locale[:2] + locale[2:].upper()
        if len(locale) == 2:
            locale = self._find_locale_for_lang(locale)
        if locale not in LOCALES_AVAILABLE:
            log('citationstyles locale not found for {0}.  '
                'Falling back to default.'.format(locale))
            # fall back to global default
            locale = DEFAULT_LOCALE
        locale_string = self._get_locale_string(locale)
        return 'collective_csl_info.add_locale({0}, {1});'.format(
            dumps(locale), dumps(locale_string))

    @staticmethod
    def _find_locale_for_lang(lang):
        """Attempt to find an available locale for a non-country
        specific language."""
        for locale in LOCALES_AVAILABLE:
            if locale.startswith(lang):
                return locale
        return lang

    def _get_locale_string(self, locale):
        locale_fname = 'locales-{0}.xml'.format(locale)
        locale_file = os.path.join(LOCALES_DIR, locale_fname)
        with open(locale_file,'rb') as f:
            data = f.read()
        return data

    @staticmethod
    def render_base():
        return BASE_JS

    def __call__(self):
        """Render everything"""
        self._setHeader()
        output = []
        output.append(self.render_base())
        output.append(self.render_csl())
        output.append(self.render_locales())
        return '\n'.join(output)
