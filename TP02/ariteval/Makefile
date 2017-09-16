MAINFILE = arit2
PACKAGE = Arit2
MYNAME = JohnDoe

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif

all: antlr

antlr: $(PACKAGE).g4
	$(ANTLR4) $< -Dlanguage=Python3

run: $(MAINFILE).py
	python3 $<

tests: check_ariteval.py
	python3 $< -q . testfiles/*.txt

tar: clean
	cd ..; tar cvfz $(MYNAME).tgz ariteval/ --transform 's/ariteval/$(MYNAME)/'

clean:
	rm -rf *~ $(PACKAGE)*.py $(PACKAGE)*.pyc *.tokens  __pycache*
