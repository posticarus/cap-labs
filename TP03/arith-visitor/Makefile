PACKAGE = Arit
MAINFILE = arit
ANTLR4 = java -jar /home/laure/Installs_boulot/antlr-4.7-complete.jar

all: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor

run: $(MAINFILE).py
	python3 $^

ex: $(MAINFILE).py
	python3 $^ < myexample


clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
