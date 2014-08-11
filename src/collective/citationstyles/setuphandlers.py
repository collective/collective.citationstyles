from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from collective.citationstyles.interfaces import ISettings
from collective.citationstyles import DEFAULT_CSL


def _set_default_style(site):
    """only set default style if it is not already set"""
    registry = getUtility(IRegistry)
    csl_settings = registry.forInterface(ISettings)
    # only set the default style for the site if it hasn't already been set.
    if not csl_settings.default_style:
        csl_settings.default_style = DEFAULT_CSL


def setupVarious(context):
    """handle customized setup for collective.citationstyles"""
    if context.readDataFile('collective.citationstyles.txt') is None:
        return

    portal = context.getSite()

    _set_default_style(portal)
