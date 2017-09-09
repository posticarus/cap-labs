PACKAGE = ITE
MAINFILE = main
ANTLR4 = java -jar /home/laure/Installs_boulot/antlr-4.7-complete.jar

all: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3

run: $(MAINFILE).py
	python3 $^ 

clean:
	rm -rf *~ $(PACKAGE)*.py $(PACKAGE)*.pyc *.tokens  __pycache*
