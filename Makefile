install:
	pyenv install 3.10.11
	pip install -r requirements.txt

test:
	python main.py

windows-build:
	python setup.py bdist_msi

mac-build:
	python setup.py bdist_dmg