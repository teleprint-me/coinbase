venv:
	virtualenv venv
	source venv/bin/activate

setup:
	pip install -r requirements.txt

build:
	python -m build .

install:
	python setup.py install

uninstall:
	pip uninstall coinbase

clean:
	rm -rfv .pytest_cache/ dist/ coinbase.egg-info/ coinbase/__pycache__ coinbase/plugin/__pycache__
