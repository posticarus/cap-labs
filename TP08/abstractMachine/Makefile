toplevel: main.native
	mv $< $@

main.native:
	ocamlbuild -use-menhir $@


.PHONY: main.native

clean:
	rm -rf _build/ *~ toplevel
