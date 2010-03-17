#!/bin/bash
# The commands I use to package this up.


# blow away the old junk, keep things in sync.
rm MANIFEST
rm -r docs/dectools_html
rm -r docs/dectools_text
rm -r docs/latex
rm docs/dectool.pdf
find . -name "*~" -exec rm {} \;
find . -name "*.pyc" -exec rm {} \;
find . -name ".coverage" -exec rm {} \;
rm -r docs/dectools_html/.doctrees docs/dectools_text/.doctrees

# run nosetests, just to be sure my units are up to date
nosetests
find . -name "*.pyc" -exec rm {} \;

# make the documentation
sphinx-build -E -b html docs/sphinx docs/dectools_html/
sphinx-build -b text docs/sphinx docs/dectools_text/
echo "EDIT FILES IN THE ../sphinx DIRECTORY NOT HERE" > docs/dectools_html/_sources/README
echo "EDIT FILES IN THE ../sphinx DIRECTORY NOT HERE" > docs/dectools_html/_static/README
echo "EDIT FILES IN THE ../sphinx DIRECTORY NOT HERE" > docs/dectools_text/README
sphinx-build -E -b latex docs/sphinx docs/latex
(cd docs/latex; make all-pdf)
mv docs/latex/dectools.pdf docs
rm -r docs/latex
rm -r docs/dectools_html/.doctrees docs/dectools_text/.doctrees
#git add .
#git commit
#git push origin master
#python setup.py register sdist upload
echo "All done."
