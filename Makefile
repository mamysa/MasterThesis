genpdf:
	pdflatex --shell-escape thesis.tex

bib:
	bibtex thesis

venv:
	python3 -m venv ~/.venv/thesisdeps
	echo . ~/.venv/thesisdeps/bin/activate > venv
	. ./venv && python3 -m pip install pygments

.PHONY: clean

clean:
	rm -rf _minted-thesis
	rm -f *.lof
	rm -f *.log
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.toc
	rm -f *.out
	rm -f *.pdf
