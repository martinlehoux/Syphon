test: env
	. env/bin/activate
	ENV=test python -m pytest

lint: env
	. env/bin/activate
	isort --atomic *.py
	pylint *.py

serve: env
	. env/bin/activate
	ENV=dev ./app.py

nserve: env
	. env/bin/activate
	ENV=dev ./app.py 192.168.0.12

install:
	virtualenv env
	. env/bin/activate
	pip install -r requirements.txt

shell: env
	. env/bin/activate
	ENV=dev python
