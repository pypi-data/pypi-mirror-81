.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=========================
visaplan.zope.inputmacros
=========================

Generic METAL macros for input fields

This package uses the TAL_ / METAL_ XML-based template language introduced by
Zope_ to provide simple input fields from Python dictionaries,
without any connection to schema data whatsoever.


Features
--------

- Forms built by `div` or `table` elements
- `readonly` fields
- `required` fields
- labels


Examples
--------

This add-on is currently under development and not yet used on public internet
sites.


Documentation
-------------

After installing, you may try the views

- formfields_div_
- formfields_table_

in your Zope instance; the macros are "self-documenting".

*Note:* Currently it helps to understand German;
those views are not (yet?) internationalized.


Installation
------------

Install visaplan.zope.inputmacros by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.zope.inputmacros


and then running ``bin/buildout``


Requirements
------------

You'll need a language interpreter as well; this will be given in default
Zope / Plone installations.
We don't specify this here to allow you to choose your own.

Starting with Plone 5, Chameleon_ is used;
please use this for from-scratch use, and tell us about any problems you might
suffer (since we didn't try yet ourselves.)


Contribute
----------

- Issue Tracker: https://github.com/visaplan/zope.inputmacros/issues
- Source Code: https://github.com/visaplan/zope.inputmacros


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

.. _`issue tracker`: https://github.com/visaplan/zope.inputmacros/issues
.. _Chameleon: https://pypi.org/project/Chameleon/
.. _formfields_div: http://localhost:8080/Plone/formfields_div
.. _formfields_table: http://localhost:8080/Plone/formfields_table
.. _METAL: https://en.wikipedia.org/wiki/Template_Attribute_Language#METAL
.. _TAL:  https://en.wikipedia.org/wiki/Template_Attribute_Language
.. _Zope: https://pypi.org/project/Zope/

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
