from dictionary.models import *
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404

import string

import logging
log = logging.getLogger(__name__)

def get_def_for_tooltip(term, context):
    "Get a dictionary definition for (i) tooltips in the OPUS UI"
    try:
        definition = (Definition.objects.using('dictionary')
                      .select_related()
                      .filter(context=context,
                              term=term).values('definition',
                                                'term',
                                                'context__description').first())
        return definition
    except Definition.DoesNotExist:
        return None

def get_more_info_url(term, context):
    "Return the url of the page for this definition."
    if get_def_for_tooltip(term, context):
        return "http://pds-rings.seti.org/__dictionary/index.php?term=%s&context=%s" % (term, context)
    else:
        return None

def api_get_definition_list(request):
    "Return an alphabetical list of definitions for a single prefix letter."
    alpha = request.GET.get('alpha', None)
    if alpha is None:
        return JsonResponse({'error': 'No alpha given'})
    definitions = (Definition.objects.using('dictionary').select_related()
                   .filter(term__istartswith=alpha)
                   .values('definition', 'term', 'import_date',
                           'context__description').order_by('term'))
    return JsonResponse(list(definitions), safe=False)

def api_display_definitions(request):
    alphabetlist = list(string.ascii_uppercase)
    return render(request,
                  'dictionary/dictionary.html',
                  {'alphabetlist': alphabetlist})

def api_display_definition(request):
    term = request.GET.get('term', None)
    if term is None:
        raise Http404
    try:
        definition = (Definition.objects.using('dictionary')
                      .select_related()
                      .filter(context=context,
                              term=term).values('definition',
                                                'term',
                                                'context__description').first())
        return definition
    except Definition.DoesNotExist:
        return False

    return render(request, 'dictionary/dictionary.html', {'alphabetlist':alphabetlist})


def api_search_definitions(request):
    """
        User can search the definition database for words w/in the definitions.
        Not currently enabled to search on term
    """
    term = request.GET.get('term', None)
    if term is None:
        return JsonResponse({'error': 'No term given'})
    try:
        definitions = (Definition.objects.using('dictionary').select_related()
                       .filter(definition__icontains=term)
                       .values('definition', 'term', 'import_date',
                               'context__description').order_by('term'))
        return JsonResponse(list(definitions), safe=False)
    except Definition.DoesNotExist:
        log.info('Dictionary search for "%s" returned nothing',
                 slug)
        return JsonResponse({'error': 'Search string "'+slug+'" not found'})

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.

    this seems like a util! #todo
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s
