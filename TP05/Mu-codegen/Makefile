PACKAGE = Mu
MAINFILE = Main
FOO?=../tests/test01.mu
ASM=$(FOO:%.mu=%.s)
OBJ=$(FOO:%.mu=%.obj)
TRACE=$(FOO:%.mu=%.trace)
SIMU=../../../leia/simu
ASSEMBLER=../../../leia/asm.py


ifndef ANTLR4
abort:
	$(error variable ANTLR4 is not set)
endif


all: antlr run

antlr: $(PACKAGE).g4 
	$(ANTLR4) $< -Dlanguage=Python3 -visitor -no-listener

.PHONY: run
run: $(ASM)
$(ASM): ${wildcard *.py} $(FOO)
	python3 $(MAINFILE).py $(FOO)

$(OBJ): $(ASM)
	python3 $(ASSEMBLER) $<

.PHONY: trace
trace: $(TRACE)
	cat $<
$(TRACE): $(OBJ) $(SIMU)
	$(SIMU) q $(OBJ) >$@

$(SIMU):
	cd $(dir $(SIMU)) && $(MAKE)

clean:
	rm -rf *~ $(PACKAGE)*.py *.pyc *.tokens  __pycache*
	rm -f ../tests/*.s ../tests/*.obj ../tests/*.s ../tests/*~

../../TP04/Mu-evalntype/MuParser.py:
	make -C ../../TP04/Mu-evalntype/

../../leia/simulateur/LEIA:
	make -C ../../leia/simulateur/

tests: ../../TP04/Mu-evalntype/MuParser.py ../../leia/simulateur/LEIA antlr
	python3 ./test_leia_api.py
	python3 -m pytest -v ./test_codegen.py
