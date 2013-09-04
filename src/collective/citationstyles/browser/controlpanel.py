from lxml import etree
from zope.component import getMultiAdapter
from zope.component import getUtility

from AccessControl import Unauthorized

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.decode import processInputs
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.controlpanel.form import ControlPanelView
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry

from collective.citationstyles.interfaces import ISettings
from collective.citationstyles import citationstylesMessageFactory as _

class SettingsControlPanelView(ControlPanelView):

    label = _(u'Citation Styles')
    description = _(u'Use this control panel to upload '
                    'citation styles in CSL format and '
                    'select the default style for the '
                    'site.')


    def __call__(self):
        if self.update():
            return self.index()
        return ''

    def update(self):
        processInputs(self.request)

        self.errors = {}
        submitted = False
        form = self.request.form
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)

        if 'form.button.Cancel' in form:
            IStatusMessage(self.request).add(_(u'Changes canceled.'))
            portal_url = getToolByName(self.context, 'portal_url')()
            self.request.response.redirect("%s/plone_control_panel"%
                                           portal_url)
            return False

        if 'form.button.Save' in form:
            self.authorize()
            submitted = True
            default = form.get('default_style', None)
            settings.default_style = default
            style_file = form.get('csl_file', None)
            if style_file is not None and style_file.filename:
                citation_styles = settings.citation_styles
                if citation_styles is None:
                    citation_styles = {}
                style = etree.parse(style_file).getroot()
                style_info = style.find('{http://purl.org/net/xbiblio/csl}info')
                style_id = unicode(style_info.find('{http://purl.org/net/xbiblio/csl}title').text)
                citation_styles[style_id] = unicode(etree.tostring(style))
                settings.citation_styles = citation_styles

        if submitted and not self.errors:
            IStatusMessage(self.request).add(u"Updated citation styles")
        elif submitted:
            IStatusMessage(self.request).add(_(u"There were errors"), 'error')

        return True

    @property
    def default_style(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        return settings.default_style

    @memoize
    def selectable_styles(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        citation_styles = settings.citation_styles
        if citation_styles is None:
            return []
        styles = []
        for style in citation_styles.keys():
            styles.append({'id': style, 'title': style})
        return styles

    def authorize(self):
        authenticator = getMultiAdapter((self.context, self.request),
                                        name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized
