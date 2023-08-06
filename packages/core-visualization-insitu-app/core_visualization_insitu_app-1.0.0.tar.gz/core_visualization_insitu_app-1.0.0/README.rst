=============================
Core Visualization Insitu App
=============================

Visualization feature for the curator core project.


Configuration
=============

1. Add "core_visualization_insitu_app" to your INSTALLED_APPS setting like this
-------------------------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
        ...
        "core_visualization_insitu_app",
    ]

2. Include the core_visualization_insitu_app URLconf in your project urls.py like this
--------------------------------------------------------------------------------------

.. code:: python

    re_path(r'^visualization-insitu/', include("core_visualization_insitu_app.urls")),
