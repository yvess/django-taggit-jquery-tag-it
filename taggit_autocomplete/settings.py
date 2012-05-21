from django.conf import settings

# Both settings must be lists or tuples of URLs
CSS = getattr(settings, 'TAGGIT_AUTOCOMPLETE_CSS', ''),
JS = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JS', [])
JS.append(settings.STATIC_URL +
                              'taggit_autocomplete/js/tag-it.js')
