# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS       ?=
SPHINXBUILD      ?= sphinx-build
SPHINXVERBUILD   ?= sphinx-multiversion
SOURCEDIR        = source
BUILDDIR         = build

# Put it first so that "make" without argument is like "make all".
all: Makefile
	make clean
	make html
	make xml
	make rst
#	make markdown

.PHONY: help Makefile both

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
