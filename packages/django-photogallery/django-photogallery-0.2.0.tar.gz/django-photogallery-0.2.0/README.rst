============
Photogallery
============

Photogallery is Django app to allow users to look through pictures 
and posts created by admin.

Quick start
-----------
1. Install photogallery::
    
    pip install django-photogallery

2. Add "photogallery" to INSTALLED_APPS::
    
    INSTALLED_APPS = [
        ...
        'photogallery',
    ]

3. Add photogallery URLconf to urls.py::

    path('photogallery/', include('photogallery.urls')),

4. Run ``python manage.py migrate`` to create models.

5. Start the server and add post on http://127.0.0.1:8000/admin/ after enabling Admin app.

6. Visit http://127.0.0.1:8000/photogallery/ to look through all added picture posts.
