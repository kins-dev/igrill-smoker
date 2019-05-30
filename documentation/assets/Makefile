# Makefile for building SVG files from mmd files

all: monitor.svg data.svg start_smoking.svg config.svg

%.svg: %.mmd
	mmdc -i $^ -o $@

clean:
	$(RM) $(TARGET).svg