PACKAGE = AritPlot
MAINFILE = arit
FOO?=ex/ex01.txt

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif


all: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor


run: $(MAINFILE).py
	python3 $^  $(FOO)

clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
