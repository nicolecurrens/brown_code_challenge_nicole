# Installation

I followed the installation instructions from the template repo. You will need to clone the repository and create a virtual environment (if you haven't already). Then install the requirements:

```bash
$ source ../venv/bin/activate
(venv) $ pip install pip-tools
(venv) $ pip-compile ./config/requirements/requirements_base.in
(venv) $ pip install -r ./config/requirements/requirements_base.txt
(venv) $ python -m spacy download en_core_web_sm
(venv) $ python ./manage.py runserver
```

I added two requirements to the requirements_base.in file for my project, `djangorestframework` and `spacy`. 

[DRF](https://www.django-rest-framework.org/) provides some useful tools for handling requests and responses. [Spacy](https://spacy.io/) is a natural language processing library, which I used to run named entity recognition on some of the metadata from the [Brown API](https://repository.library.brown.edu/studio/api-docs/). Spacy requires you to download a model to use. I chose en_core_web_sm, which is a commonnly used small English model. 

## A note on the project structure
I use GitHub Desktop to manage my git workflow. Unfortunately, GitHub Desktop didn't play well with the `update_project_and_app_references.py` script for a few reasons **. I find that Github Desktop makes my development process faster, and I didn't want to spend too much time for it on this project. But this is the reason for the odd outer directory in this project - this is not something I would normally do. I'm sure that given enough time there is a way to make them play well together.

(** If you're curious, it can only create a .git in empty directories, and for some reason wouldn't track the files that were already in the folder when I added .git.)

---

# Using the app
The goal of this app was to create a browsing experience similar to Wikipedia or [stumble upon](https://www.stumbleupon.com/) with the Brown API. Users can click through related items from Brown's repository. When they find one they are interested in, they can view the item on Brown's website.

This app adds two related endpoints to the base template which make use of the Brown API. The first is the item detail page at `/items/<id>/`. This page returns the primary title and abstract of the item with the specified ID using data from the Brown `/items` endpoint. It also links to the item in Brown's website, so you can view the item there. If you need an ID to get started, you can use `bdr:80246`.

On the item detail page, you will see a link to related items. When you click the link, the view uses spacy to pull out the named entities from the primary title and abstract of the current item. Then, it uses the `/search` endpoint provided by Brown to search on those named entities and find other items that mention the same entities. I am assuming that Brown's solr is ranking results in some reasonable way, so that the first items returned are the most relevant to the search.

If the item is not found, the item detail page will still display the item with no metadata. If the related items are not found (because the item pid is not valid or because the primary title and abstract have no entities), a page will display informing the user that there are no related items.

These endpoints should be viewable in a browser or can be returned as json by adding `?format=json` to the URL.

---

# Motivation
I studied linguistics and I love finding ways to use tools like spacy to supplement metadata. For this project, I wanted to show a relatively simple example of this by using named entity recogntion. I noticed that one of the attributes returned by the Brown API is `keywords`, which returns a search URL with a few key words that sum up the item's metadata. I think that using named entity recognition could be a great way to add to those keywords, or create them if they don't already exist.
