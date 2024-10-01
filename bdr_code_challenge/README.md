# Setup

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

[DRF](https://www.django-rest-framework.org/) provides some useful tools for handling requests and responses. [Spacy](https://spacy.io/) is a natural language processing library, which I used to run named entity recognition on some of the metadata from the [Brown API](https://repository.library.brown.edu/studio/api-docs/).

---

# Using the app

This app adds two related endpoints to the base template which make use of the Brown API. The first is the item detail page at `/items/<id>/`. This page returns the primary title and abstract of the item with the specified ID using data from the Brown `/items` endpoint. If you need an ID to get started, you can use `bdr:80246`.

On the item detail page, you will see a link to related items. When you click the link, the view uses spacy to pull out the named entities from the primary title and abstract of the current item. Then, it uses the `/search` endpoint provided by Brown to search on those named entities and find other items that mention the same entities.

If the item is not found, the item detail page will display 

---
