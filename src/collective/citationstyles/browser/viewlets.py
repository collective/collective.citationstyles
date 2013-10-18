from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFBibliographyAT.interface import IBibliographicItem
from Products.CMFBibliographyAT.interface import IBibliographyFolder
from Products.CMFBibliographyAT.interface import ILargeBibliographyFolder


class CiteprocSetupViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('citeproc_setup.pt')
    
    script_template = """
<script>
$(document).ready( function() {
    var bib_replaceable = $('.cmfbib_entry');
    if (collective_csl_info === undefined) {
        return;
    }
    bib_replaceable.hide();
    $.getJSON('%s', function (data, status, xhr) {
        var output, insertable, entry_id, link, entry;
        if (data.error !== undefined) {
            bib_replaceable.show();
            return;
        }
        collective_csl_info.set_references(data);
        citeproc = new CSL.Engine(collective_csl_info, collective_csl_info.retrieveCSL());
        citeproc.updateItems(collective_csl_info.reference_keys());
        citeproc.setAbbreviations("default");
        output = citeproc.makeBibliography();
        if (output && output.length && output[1].length) {
            insertable = $(output[0].bibstart + output[0].bibend);
            bib_replaceable.filter(':first').before(insertable);
            for (i=0; i<output[1].length; i++) {
                entry_id = output[0].entry_ids[i][0];
                entry = $(output[1][i]);
                link = $('<a class="cmfbib_entry_link">');
                found = $('a[uid="' + entry_id + '"]')
                // iterator may return items not found on page (because of
                // batching); safely handle missing items by ignoring.
                if (found.length) {
                    link.attr('href', found.attr('href'))
                        .text('more information about this reference');
                    if (link.attr('href')) {
                        link.appendTo(entry);
                    }
                    entry.appendTo(insertable);
                } else if (output[1].length == 1) {
                    entry.appendTo(insertable);
                }
            }
            bib_replaceable.remove();
        } else {
            bib_replaceable.show();
        }
    });
});
</script>
"""

    def available(self):
        if (IBibliographicItem.providedBy(self.context) or
            IBibliographyFolder.providedBy(self.context) or
            ILargeBibliographyFolder.providedBy(self.context)):
            return True
        return False

    def script(self):
        json_url = self.context.absolute_url() + '/@@citations-json'
        return self.script_template % json_url
