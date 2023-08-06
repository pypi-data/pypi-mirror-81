Wagtail Person
==============

On a CMS, we regularly need to represent an author, a speaker, a
person. To avoid repetition and duplication of datas about this, this
app add a person model to Wagtail, with admin UI. Do not hesitate to
use it on your blog or lectures appilaciton.

This model is accompanied by a Person page model and a Persons index
page model. Each Person page is linked to a Person model to see it on
your website.

This app also provide a basic CSS and templates, feel free to
customize it.


Important
---------

Since version 0.9.8, the Person Page model has been split in 2 models:
- A Person model
- A Person page model, with a many2one to a Person model


Install
-------

Simply install it from pypi.org:

``` {.bash}
pip install wagtailperson
```

Add this app to django installed app in your settings.py:

``` {.python}
INSTALLED_APPS = [
    # …
    'wagtailperson',
    # …
    'wagtail.contrib.modeladmin',
    # …
    ]
```

Then, finally, apply migration scripts:

``` {.bash}
./manage.py migrate wagtailperson
```


Use
---

This application add a new entry to the administration menu, called
"Author or Person". From this menu, you can add a new author or
person.

If you want to link one of your wagtail page models, or django models,
to a person: Simply add a many2one field linked to
`wagtailperson.models.Person`.

This application also provide 2 pages models:

-   A Person page: Show puplicly someone, can be used mostly
    everywhere in the pages tree
-   A Persons index page: A root page for Persons pages, it list each
    of Persons pages it had as children pages and can only have Person
    pages as children

The person index page can be useful to group persons, globally or per
group.

A person got multiple fields:
-   Picture
-   Name
-   Tags
-   Introduction
-   Abstract

This application also provide a person block for StreamField, at
`wagtailperson.blocks.PersonBlock`. Feel free to use it on your models
StreamField.


Development
-----------

The source code repository provide a full Django project, so you can
easily work with wagtailperson for testing you modifications.

Simply use these two steps in the source code working directory:

``` {.bash}
./manage.py migrate
./manage.py runserver
```


Licence
-------

LGPLv3


Author
------

Sébastien Gendre \<seb\@k-7.ch\>
