test: env
	. env/bin/activate
	python -m pytest

lint: env
	. env/bin/activate
	isort --atomic *.py
	pylint *.py

serve: env
	. env/bin/activate
	./app.py

install:
	virtualenv env
	. env/bin/activate
	pip install -r requirements.txt
