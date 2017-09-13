PACKAGE = AritPlot
MAINFILE = arit
FOO?=ex/ex01.txt

ANTLR4=java -jar ~/Installs_boulot/antlr-4.7-complete.jar

all: $(PACKAGE).g4
	$(ANTLR4) $^ -Dlanguage=Python3 -visitor

#ANTLR_MK = ../../../antlr/
#include $(ANTLR_MK)/antlr.mk
#this file doesn't exist in the repo


run: $(MAINFILE).py
	python3 $^  $(FOO)

clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
