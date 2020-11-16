#!/bin/bash

DOCS_SOURCE="docsrc/"
DOCS_HTML="docs/"

# Go into the Docs source directory
cd $DOCS_SOURCE
# Clean the old source
make clean && make clean-github
# Build the new documentation
make github
# Go back to where we started
cd ..
# Update git with the updates
git add -u
