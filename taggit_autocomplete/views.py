from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import simplejson

from taggit.models import Tag

def list_tags(request):
	try:
		tags = Tag.objects.filter(name__icontains=request.GET['term']).values_list('name', flat=True)
	except MultiValueDictKeyError:
		pass
	tags = list(tags)
	return HttpResponse(simplejson.dumps(tags), mimetype='text/javascript')
