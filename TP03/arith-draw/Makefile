PACKAGE = AritPlot
MAINFILE = arit
MYNAME = JohnDoe

FOO?=ex/check01.txt

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif


$(PACKAGE)Listener.py $(PACKAGE)Visitor.py $(PACKAGE)Lexer.py $(PACKAGE)Lexer.tokens $(PACKAGE)Parser.py $(PACKAGE).tokens: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor

main-deps: $(PACKAGE)Lexer.py $(PACKAGE)Parser.py MyAritPlotVisitor.py

run: $(MAINFILE).py main-deps
	@python3 $^  $(FOO)


# tests all files in the ex/ directory
tests: test_aritplot.py main-deps
	python3 $< 


tar: clean
	cd ..; tar cvfz $(MYNAME).tgz arit-draw/ --transform 's/ariteval/$(MYNAME)/'


clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
