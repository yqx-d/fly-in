FNAME = main.py
MODULES = flake8 mypy pygame


run:
	python3 $(FNAME)

install:
	pip install $(MODULES)

debug:
	python3 -m pdb $(FNAME)

clean:
	rm -rf __pycache__ .mypy_cache *.pyc

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict
