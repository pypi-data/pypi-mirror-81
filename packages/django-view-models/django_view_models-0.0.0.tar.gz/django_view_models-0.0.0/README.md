# django_view_models

Designed for Postgres. May or may not work with other databases.

## Installation/Usage
- `pip install django_view_models`
- add `django_view_models` to `INSTALLED_APPS`
- define view models (see below)
- `python manage.py sync_view_models` (run after every view definition change)

## Defining View Models

You must define the fields on your model, and either define `VIEW_DEFINITION` or `view_query` on your model. 

Note that just like regular models, django will add an integer primary key called `id`, unless you set `primary_key=True` on one of your fields.

```python
from django.db import models
from django_view_models.models import ViewModel, MaterializedViewModel

class Book(models.Model):
    title = models.TextField()
    is_good = models.BooleanField()

# create a ViewModel with a manual query
class GoodBook(ViewModel):
    title = models.TextField()

    VIEW_DEFINITION = '''
        SELECT id, title
        FROM my_app.book
        WHERE is_good = true
    '''

# create a ViewModel, and use Django's ORM to create the query
class BadBook(ViewModel):
    title = models.TextField()

    def view_query():
        return Book.objects.filter(is_good=False).values('id', 'title')
```