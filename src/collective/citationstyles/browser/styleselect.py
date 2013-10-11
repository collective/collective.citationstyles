from zope import interface, schema
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable

from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form

from Products.statusmessages.interfaces import IStatusMessage

from collective.citationstyles import citationstylesMessageFactory as _
from collective.citationstyles.config import STYLESHEET_SELECTED_KEY

class IStylesheetSelect(interface.Interface):
    stylesheet = schema.Choice(
            __name__="style",
            title=_(u'Style'),
            description=_(u'Select the style to use for citations.'),
            required=True,
            vocabulary=u'collective.citationstyles.vocabularies.SelectableStylesheets'
            )

class StylesheetSelectForm(form.Form):
    fields = field.Fields(IStylesheetSelect)
    label = _(u"Citations Style")
    description = _(u"Style for citations.")

    def getContent(self):
        annotations = IAnnotations(self.context)
        curr_style = annotations.get(STYLESHEET_SELECTED_KEY)
        return { 'style': curr_style }

    @button.buttonAndHandler(u'Select Style')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        assert IAttributeAnnotatable.providedBy(self.context)
        annotations = IAnnotations(self.context)
        annotations[STYLESHEET_SELECTED_KEY] = data['style']

        self.request.response.redirect(self.context.absolute_url())
        messages = IStatusMessage(self.request)
        messages.add(_(u"Citation style set: ") + data['style'], type=u"info")


StyleSelectView = wrap_form(StylesheetSelectForm)
