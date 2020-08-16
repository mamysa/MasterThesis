genpdf:
	pdflatex --shell-escape thesis.tex

venv:
	python3 -m venv ~/.venv/thesisdeps
	echo . ~/.venv/thesisdeps/bin/activate > venv
	. ./venv && python3 -m pip install pygments
