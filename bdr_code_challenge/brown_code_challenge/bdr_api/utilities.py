""" Utility functions for views """

import requests
from rest_framework.response import Response
from rest_framework import status
import json, logging

log = logging.getLogger(__name__)

BASE_API_URL = 'https://repository.library.brown.edu/api/'

def make_bdr_call(category, id):
    """ Function to make generic BDR API calls 

    category (string): whether to call the items or collections API
    id (string): id of the collection/item to GET

    returns: An error, or a dictionary containing the item/collection data

    """
    if category not in ['items', 'collections']:
        log.debug('Category in request incorrectly specified.')
        return Response("Must specify 'items' or 'collections'", status=status.HTTP_400_BAD_REQUEST)

    try:
        if category == 'items':
            log.info('Making call to /items.')
            resp = requests.get(f"{BASE_API_URL}/items/{id}")
        else:  # Collections
            log.info('Making call to /collections.')
            resp = requests.get(f"{BASE_API_URL}/collections/{id}")

        resp.raise_for_status()
        return json.loads(resp.text)

    except requests.exceptions.ConnectionError:
        return Response("Connection error occurred. Please try again later.", status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.exceptions.Timeout:
        return Response("The request timed out. Please try again later.", status=status.HTTP_504_GATEWAY_TIMEOUT)
    except requests.exceptions.RequestException as e:
        return Response(f"An error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_query( entities ):
    """
    Given a list of strings, construct a solr query.

    entities (list): A list of the named entities to include in the query

    returns: a search string formatted for solr
    ex. 'Test'%20OR%20'Brown'
    """
    search_string = ""
    for word in entities:
        # %20 is for URL encoding
        search_string = search_string + "\'" + str(word) + "\'%20OR%20"

    # Remove extra %20OR%20 from the end
    search_string = search_string[:-8]
    return search_string

def format_search_results( solr_data ):
    docs = solr_data['response']['docs']
    results = []

    for item in docs:
        item_data = {}
        item_data['pid'] = item['pid']
        item_data['name'] = item['primary_title']
        results.append(item_data)

    return results

def make_search_call( entities ):
    """ Function to make generic BDR API calls 

    query (list): list of named entities to search on

    returns: an error, or a dictionary of the 5 items returned by the search

    """
    # Validation
    if not entities:
        log.debug('Query cannot be empty.')
        return Response("Query cannot be empty.", status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(entities, list):
        log.debug('Query must be a list.')
        return Response("Query must be a list.", status=status.HTTP_400_BAD_REQUEST)

    search_string = create_query(entities)

    try:
        log.info('Making call to /search.')
        resp = requests.get(f"{BASE_API_URL}/search/?q={search_string}&rows=5&q.op=OR")

        resp.raise_for_status()

        search_results = format_search_results(json.loads(resp.text))

        return search_results

    except requests.exceptions.ConnectionError:
        return Response("Connection error occurred. Please try again later.", status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.exceptions.Timeout:
        return Response("The request timed out. Please try again later.", status=status.HTTP_504_GATEWAY_TIMEOUT)
    except requests.exceptions.RequestException as e:
        return Response(f"An error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

