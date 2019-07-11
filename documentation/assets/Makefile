# Makefile for building SVG files from mmd files

all: $(patsubst %.mmd,%.svg,$(wildcard *.mmd))

%.svg: %.mmd
	mmdc -i $^ -o $@

clean:
	$(RM) $(patsubst %.mmd,%.svg,$(wildcard *.mmd))