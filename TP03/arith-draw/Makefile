PACKAGE = AritPlot
MAINFILE = arit
MYNAME = JohnDoe

FOO?=ex/check01.txt

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif


all: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor


run: $(MAINFILE).py
	@python3 $^  $(FOO)


# tests all files in the ex/ directory
tests: test_aritplot.py
	python3 $< 


tar: clean
	cd ..; tar cvfz $(MYNAME).tgz arit-draw/ --transform 's/ariteval/$(MYNAME)/'


clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
