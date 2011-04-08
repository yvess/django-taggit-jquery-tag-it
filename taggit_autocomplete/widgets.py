from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

from utils import edit_string_for_tags


class TagAutocomplete(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        list_view = reverse('taggit_autocomplete-list')
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags(
                    [o.tag for o in value.select_related("tag")])
        html = super(TagAutocomplete, self).render(name, value, attrs)
        # change to use new jquery-ui autocomplete
        js = u"""
            <script type="text/javascript">
                (function($) {
                    $.ready(function() {
                        function split( val ) {
                            return val.split( /,\s*/ );
                        }
                        function extractLast( term ) {
                            return split( term ).pop();
                        }
                        // don't navigate away from the field on tab
                        // when selecting an item.
                        $("#%(id)s")
			                .bind( "keydown", function( event ) {
                            if ( event.keyCode === $.ui.keyCode.TAB &&
                                    $( this ).data( "autocomplete" ).menu.active ) {
                                event.preventDefault();
                            }
			            })
                        .autocomplete({
                            source: function( request, response ) {
                                $.getJSON( "%(source)s", {
                                    term: extractLast( request.term )
                                }, response );
                            },
                            search: function() {
                                // custom minLength
                                var term = extractLast( this.value );
                                if ( term.length < 2 ) {
                                    return false;
                                }
                            },
                            focus: function() {
                                // prevent value inserted on focus
                                return false;
                            },
                            select: function( event, ui ) {
                                var terms = split( this.value );
                                // remove the current input
                                terms.pop();
                                // add the selected item
                                terms.push( ui.item.value );
                                // add placeholder to get the comma-and-space
                                // at the end
                                terms.push( "" );
                                this.value = terms.join( ", " );
                                return false;
                            }
                        });
                    });
                })(django.jQuery);
            </script>
            """ % ({'id':attrs['id'], 'source':list_view})
        return mark_safe("\n".join([html, js]))

    class Media:
        js_base_url = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JS_BASE_URL',
                              '%s/jquery-autocomplete' % settings.MEDIA_URL)
        css = {
            'all': ('%s/jquery.autocomplete.css' % js_base_url,)
        }
        js = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JQUERYUI_JS', [])
        
