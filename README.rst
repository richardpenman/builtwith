================
Reverse Engineer
================

Detect the technology used by a website, such as Apache, JQuery, and Wordpress.
Here is some example usage: ::

    $ python reverse_engineer.py http://webscraping.com
    Analytics: Google Analytics
    JavaScript framework: Modernizr
    Web server: Nginx

    $ python reverse_engineer.py http://wordpress.com
    Blog: WordPress
    CMS: WordPress
    Web server: Nginx
    
    $ python reverse_engineer.py http://microsoft.com
    JavaScript framework: Modernizr
    Web framework: Microsoft ASP.NET


=======
Install
=======

.. sourcecode:: bash

    pip install reverse_engineer

