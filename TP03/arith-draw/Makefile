PACKAGE = AritPlot
MAINFILE = arit
MYNAME = JohnDoe	#change with your own name

FOO?=ex/check01.txt

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif


$(PACKAGE)Listener.py $(PACKAGE)Visitor.py $(PACKAGE)Lexer.py $(PACKAGE)Lexer.tokens $(PACKAGE)Parser.py $(PACKAGE).tokens: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor

main-deps: $(PACKAGE)Lexer.py $(PACKAGE)Parser.py MyAritPlotVisitor.py

# tests on the file specified in the FOO variable
# write make run FOO=ex/check02.txt or edit this Makefile
run: $(MAINFILE).py
	python3 $^  $(FOO)


# tests all files in the ex/ directory
tests: test_aritplot.py main-deps
	python3 $< 

# creates an archive of your arit-draw folder with your name
tar: clean
	cd ..; tar cvfz $(MYNAME).tgz arit-draw/ --transform 's/ariteval/$(MYNAME)/'

# removes the byproducts of compilation
clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
