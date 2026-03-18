PACKAGE = a_maze_ing
MAIN    = a_maze_ing.py
PYTHON  = python3
PIP     = pip
VENV_PYTHON = .venv/bin/python
SRC		= a_maze_ing.py a_maze_ing/

all: run

run:
	$(PYTHON) $(MAIN) "config.txt"

uninstall:
	@rm -rf .venv || true

install: uninstall
	@$(PYTHON) -m venv .venv
	@. .venv/bin/activate && $(PIP) install -r requirements.txt

debug:
	$(PYTHON) -m pdb $(MAIN)

lint:
	@echo "\n-- Running flake8 --\n"
	-@$(VENV_PYTHON) -m flake8 $(SRC)
	@echo "\n-- Running mypy --\n"
	@$(VENV_PYTHON) -m mypy . \
        --exclude 'build/'\
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@echo "\n-- Running flake8 --\n"
	-@$(VENV_PYTHON) -m flake8 $(SRC)
	@echo "Running mypy"
	-@$(VENV_PYTHON) -m mypy . --strict \
        --exclude '(build|dist|\.venv)'\
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

clean:
	@rm -rf dist/ build/ *.egg-info *.tar.gz *.whl
	@rm -rf __pycache__ a_maze_ing/__pycache__ .mypy_cache

package:
	$(PYTHON) -m build
	@mv dist/*.tar.gz .
	@mv dist/*.whl .

.PHONY: all install run debug lint lint-strict clean package
