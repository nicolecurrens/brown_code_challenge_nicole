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


def make_search_call( query ):
    """ Function to make generic BDR API calls 

    category (string): whether to call the items or collections API
    id (string): id of the collection/item to GET

    """
    # Validation
    if not query:
        log.debug('Query cannot be empty.')
        return Response("Query cannot be empty.", status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(query, str):
        log.debug('Query must be a string.')
        return Response("Query must be a string.", status=status.HTTP_400_BAD_REQUEST)

    try:
        log.info('Making call to /search.')
        resp = requests.get(f"{BASE_API_URL}/search/?{query}")

        resp.raise_for_status()

        return resp.text
    
    except requests.exceptions.ConnectionError:
        return Response("Connection error occurred. Please try again later.", status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except requests.exceptions.Timeout:
        return Response("The request timed out. Please try again later.", status=status.HTTP_504_GATEWAY_TIMEOUT)
    except requests.exceptions.RequestException as e:
        return Response(f"An error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)