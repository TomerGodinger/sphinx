# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS              ?=
SPHINXBUILD             ?= BUILDING_DOCS=1 sphinx-build
SPHINXVERBUILD          ?= BUILDING_DOCS=1 sphinx-multiversion
SOURCEDIR               = docs/source
BUILDDIR                = docs/build-single
BUILDDIR_VERSIONS       = docs/build

GHPAGESBUILD            = html/

# Put it first so that "make" without argument is like "make all".
all: Makefile
	make clean
	make html
#	make xml
#	make rst
	make versioned
#	make markdown

ghpages:
	@$(SPHINXVERBUILD) "$(SOURCEDIR)" "$(GHPAGESBUILD)"

.PHONY: help Makefile clean clean-single clean-versions clean-ghpages

versioned:
	@$(SPHINXVERBUILD) "$(SOURCEDIR)" "$(BUILDDIR_VERSIONS)" $(SPHINXOPTS) $(O)

clean: clean-single clean-versions clean-ghpages

clean-single:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean-versions:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR_VERSIONS)" $(SPHINXOPTS) $(O)

clean-ghpages:
	rm -rf "$(GHPAGESBUILD)"

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
