SPHINXBUILD?=poetry run sphinx-build
SPHINXOPTS?=--fresh-env --write-all
SOURCEDIR=src
BUILDDIR=_build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
