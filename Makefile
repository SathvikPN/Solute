pkg_files = $(wildcard solute/*.py)
timestamp = $(shell date)

docs = .latestDocBuild

# Add @ to the beginning of command to tell gmake not to print the command being executed.
.latestDocBuild: $(pkg_files)
	@pdoc -o docs --html --force solute
	@mv docs/solute/* docs/
	@rmdir docs/solute 
	@echo "$(timestamp)" > $@

# Use .PHONY to mark targets that don’t correspond to files.
.PHONY: docs 
