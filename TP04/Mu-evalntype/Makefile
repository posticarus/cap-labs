PACKAGE = Mu
MAINFILE = Main
#change with your own name:
MYNAME = JohnDoe


FOO?=../ex/test00.mu

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif

all: run

MuLexer.py MuParser.py: $(PACKAGE).g4
	$(ANTLR4) $< -Dlanguage=Python3 -visitor -no-listener

main-deps: MuLexer.py MuParser.py MyMuVisitor.py MyMuTypingVisitor.py

run: $(MAINFILE).py main-deps
	python3  $< $(FOO)

# creates an archive of your ex folder with your name
tar: clean
	cd ..; tar cvfz Lab4-$(MYNAME).tgz ex/ --transform='s/ex/Lab4-ex-$(MYNAME)/'


# tests all files in ../ex/test*.mu
tests: test_evaluator.py main-deps
	python3 -m pytest -v $< 


clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache* ../ex/*~ .cache*
