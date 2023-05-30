all:
	pdflatex coling2020.tex
	bibtex coling2020
	pdflatex coling2020.tex
	pdflatex coling2020.tex
view:
	okular coling2020.pdf
clean:
	rm -rf *.{aux,bbl,blg,out,log}
again:
	make clean
	make all