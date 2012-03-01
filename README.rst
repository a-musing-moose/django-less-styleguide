=====================================
Django Style Guide Generator for LESS
=====================================

This is a little app the reads in the projects LESS files and automatically
generates a style guide page for variables.

At present it is pretty dumb - it simply extracts all variable assignments.

Configuration
-------------

Edit your ``settings.py`` to set the following settings::

    STYLEGUIDE_PATH = "/path_to_your_less_files"
    
You will also need to add ``styleguide`` to you list of installed apps and
add ``styleguide.urls`` to your url config.

Changelog
=========

[0.0.1] 2012-03-01
------------------

Initial commit