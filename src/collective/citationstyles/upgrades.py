from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from collective.citationstyles.interfaces import ISettings


DEFAULT_STYLES = [
    u'Modern Language Association 7th edition',
    u'American Psychological Association 6th edition',
    u'Chicago Manual of Style 16th edition (note)',
]


def upgrade_csl(context):
    """upgrade the three default csl stylesheets

    Do not alter any customizations made in the site.
    """
    registry = getUtility(IRegistry)
    csl_settings = registry.forInterface(ISettings)
    # get current settings:
    installed_default = csl_settings.default_style
    additional_styles = {
        k: v for k, v in csl_settings.citation_styles.items()
        if k not in DEFAULT_STYLES
    }
    # run profile to update three default stylesheets:
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        u'profile-collective.citationstyles:default',
        u'plone.app.registry'
    )

    # re-apply previous default style and add customizations back in
    csl_settings.default_style = installed_default
    csl_settings.citation_styles.update(additional_styles)
