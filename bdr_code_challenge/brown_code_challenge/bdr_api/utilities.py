""" Utility functions for views """

import requests

BASE_API_URL = 'https://repository.library.brown.edu/api/'

def make_bdr_call( category, id ):
    """ Function to make generic BDR API calls 

    category (string): whether to call the items or collections API
    id (string): id of the collection/item to GET

    """
    if category == 'items':
        resp = requests.get(BASE_API_URL + '/items/' + str(id))
        return resp.text
