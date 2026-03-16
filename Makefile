PACKAGE = a_maze_ing
MAIN    = a_maze_ing.py
PYTHON  = python3
PIP     = pip
SRC		= a_maze_ing.py a_maze_ing/

all: run

run:
	$(PYTHON) $(MAIN)

uninstall:
	@rm -rf .venv || true

install: uninstall
	@$(PYTHON) -m venv .venv
	@. .venv/bin/activate && $(PIP) install -r requirements.txt

debug:
	$(PYTHON) -m pdb $(MAIN)

lint:
	@echo "\n-- Running flake8 --\n"
	-@$(PYTHON) -m flake8 $(SRC)
	@echo "\n-- Running mypy --\n"
	@$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@echo "\n-- Running flake8 --\n"
	-@$(PYTHON) -m flake8 . --strict
	@echo "Running mypy"
	-@$(PYTHON) -m mypy . --strict \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

clean:
	@rm -rf dist/ build/ *.egg-info *.tar.gz *.whl
	@rm -rf __pycache__ a_maze_ing/__pycache__ .mypy_cache

package:
	$(PYTHON) setup.py sdist bdist_wheel
	@mv dist/*.tar.gz .
	@mv dist/*.whl .

.PHONY: all install run debug lint lint-strict clean package
