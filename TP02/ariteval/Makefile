MAINFILE = arit2
PACKAGE = Arit2
MYNAME = JohnDoe

ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif

$(PACKAGE)Listener.py $(PACKAGE)Lexer.py $(PACKAGE)Lexer.tokens $(PACKAGE)Parser.py $(PACKAGE).tokens: $(PACKAGE).g4
	$(ANTLR4) $< -Dlanguage=Python3

main-deps: $(PACKAGE)Lexer.py $(PACKAGE)Parser.py

run: $(MAINFILE).py main-deps
	python3 $<

tests: check_ariteval.py main-deps
	python3 $< . testfiles/*.txt

tar: clean
	cd ..; tar cvfz $(MYNAME).tgz ariteval/ --transform 's/ariteval/$(MYNAME)/'

clean:
	rm -rf *~ $(PACKAGE)*.py $(PACKAGE)*.pyc *.tokens  __pycache*
