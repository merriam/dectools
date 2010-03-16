#!/bin/bash
# The commands I use to package this up.


# blow away the old junk, keep things in sync.
rm -r docs/dectools_html
rm -r docs/latex
rm docs/dectool.pdf
find . -name "*~" -exec rm {} \;
find . -name "*.pyc" -exec rm {} \;

# run nosetests, just to be sure my units are up to date
nosetests
find . -name "*.pyc" -exec rm {} \;

# make the documentation
sphinx-build -E -b html docs/sphinx docs/dectools_html/
echo "EDIT FILES IN THE ../sphinx DIRECTORY NOT HERE" > docs/dectools_html/_sources/README
echo "EDIT FILES IN THE ../sphinx DIRECTORY NOT HERE" > docs/dectools_html/_static/README
sphinx-build -E -b latex docs/sphinx docs/latex
(cd docs/latex; make all-pdf)
mv docs/latex/dectools.pdf docs
rm -r docs/latex
