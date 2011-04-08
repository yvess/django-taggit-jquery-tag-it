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
                    $(document).ready(function() {
                        function split( val ) {
                            return val.split( /,\s*/ );
                        }
                        function extractLast( term ) {
                            return split( term ).pop();
                        }
                        function onitem(event, ui) {
                            // keep other entries for 'select'
                            // callbacks.
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
                        function noop(event, item) {
                            // don't update for focus events.
                            return false;
                        }
                        function resize(event, item) {
                            // update the width of the textinput if we need to.
                            var size = parseInt($(this).attr('size'));
                            var chars = $(this).val().length;
                            if (chars >= size) {
                                $(this).animate({width: 1.5 * chars / size *
                                $(this).width()}, 200);
                                $(this).attr('size', chars);
                            }
                            return false;
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
                            select: onitem,
                            focus: noop,
                            close: resize
                        });
                    });
                })(django.jQuery);
            </script>
            """ % ({'id':attrs['id'], 'source':list_view})
        return mark_safe("\n".join([html, js]))

    class Media:
        css = {
            'all': getattr(settings, 'TAGGIT_AUTOCOMPLETE_JQUERYUI_CSS', []),
        }
        js = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JQUERYUI_JS', [])
        
