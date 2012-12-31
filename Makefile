setup:
	@pip install --requirement=REQUIREMENTS

vms:
	@cd vagrant && vagrant destroy && vagrant up

front:
	@cd tests/functional && env PYTHONPATH=../../ python ../../provy/console.py -s test.frontend -p vagrant front-end-user=frontend

back:
	@cd tests/functional && env PYTHONPATH=../../ python ../../provy/console.py -s test.backend -p vagrant

djangofront:
	@cd tests/functional && env PYTHONPATH=../../ python ../../provy/console.py -s test.frontend -p vagrant  front-end-user=frontend django_provyfile.py

djangoback:
	@cd tests/functional && env PYTHONPATH=../../ python ../../provy/console.py -s test.backend -p vagrant django_provyfile.py

rails:
	@cd tests/functional && env PYTHONPATH=../../ python ../../provy/console.py -s test -p vagrant front-end-user=frontend rails_provyfile.py

ssh:
	@cd vagrant && vagrant ssh frontend

ssh-back:
	@cd vagrant && vagrant ssh backend

docs:
	@python docs.py

test:
	@env PYTHONHASHSEED=random PYTHONPATH=. nosetests --with-coverage --cover-package=provy --cover-erase --with-yanc --with-xtraceback tests/

build: test
	flake8 . | grep -v 'line too long'
