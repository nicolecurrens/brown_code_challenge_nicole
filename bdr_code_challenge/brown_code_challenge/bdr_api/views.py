import datetime, json, logging

import trio
import nltk
from django.conf import settings as project_settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from bdr_api.lib import version_helper
from bdr_api.lib.version_helper import GatherCommitAndBranchData
from .utilities import make_bdr_call, make_search_call
from .spacy import spacy_obj

log = logging.getLogger(__name__)


# -------------------------------------------------------------------
# main urls
# -------------------------------------------------------------------


def info( request ):
    """ The "about" view. 
        Can get here from 'info' url, and the root-url redirects here. """
    log.debug( 'starting info()' )
    ## prep data ----------------------------------------------------
    # context = { 'message': 'Hello, world.' }
    context = {
            'quote': 'The best life is the one in which the creative impulses play the largest part and the possessive impulses the smallest.',
            'author': 'Bertrand Russell' }
    ## prep response ------------------------------------------------
    if request.GET.get( 'format', '' ) == 'json':
        log.debug( 'building json response' )
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        log.debug( 'building template response' )
        resp = render( request, 'info.html', context )
    return resp


def item_detail( request, id ):
    """ The item detail view. 
        Grabs abstract and primary_title from the item data, if available.
        Displays these with a template or returns as JSON.
    """
    log.debug( 'starting item_detail()' )
    try:
        data = make_bdr_call('items', id)
    except Exception as e:
        log.error('Failed to fetch item data: %s', e)
        return HttpResponse(status=500)
    name = data.get('primary_title', None)
    abstract = data.get('abstract', None)
    context = {'id': id,
                'name': name,
                'abstract': abstract
    }

    if request.GET.get( 'format', '' ) == 'json':
        log.debug( 'building json response' )
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        log.debug( 'building template response' )
        resp = render( request, 'items.html', context )
    return resp

def related_items( request, id ):
    """ The related items view. 
        Based on { }, finds related items by querying the solr api endpoint.
        Displays these with a template or returns as JSON.
    """
    log.debug( 'starting related_items()' )
    try:
        data = make_bdr_call('items', id)
    except Exception as e:
        log.error('Failed to fetch item data: %s', e)
        return HttpResponse(status=500)

    # Grab text of useful fields to search by
    name = data.get('primary_title', None)
    abstract = data.get('abstract', None)
    # Assuming primary_title is always a string
    # and abstract is always a list
    all_text = "".join(abstract) + name

    # Get named entities from text
    spacy = spacy_obj()
    result = list(spacy.do_ner(all_text))

    

    context = {'id': id,
                'entities': result,
    }

    data = make_search_call(result)
    context['data'] = data

    if request.GET.get( 'format', '' ) == 'json':
        log.debug( 'building json response' )
        resp = HttpResponse( json.dumps(context, sort_keys=True, indent=2), content_type='application/json; charset=utf-8' )
    else:
        log.debug( 'building template response' )
        resp = render( request, 'related.html', context )
    return resp

# -------------------------------------------------------------------
# support urls
# -------------------------------------------------------------------

def error_check( request ):
    """ Offers an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug( 'starting error_check()' )
    log.debug( f'project_settings.DEBUG, ``{project_settings.DEBUG}``' )
    if project_settings.DEBUG == True:  # localdev and dev-server; never production
        log.debug( 'triggering exception' )
        raise Exception( 'Raising intentional exception to check email-admins-on-error functionality.' )
    else:
        log.debug( 'returning 404' )
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


def version( request ):
    """ Returns basic branch and commit data. """
    log.debug( 'starting version()' )
    rq_now = datetime.datetime.now()
    gatherer = GatherCommitAndBranchData()
    trio.run( gatherer.manage_git_calls )
    info_txt = f'{gatherer.branch} {gatherer.commit}'
    context = version_helper.make_context( request, rq_now, info_txt )
    output = json.dumps( context, sort_keys=True, indent=2 )
    log.debug( f'output, ``{output}``' )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def root( request ):
    return HttpResponseRedirect( reverse('info_url') )
