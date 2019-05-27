
# the build target executable:
all: monitor.svg data.svg start_smoking.svg config.svg

%.svg: %.mmd
	mmdc -i $^ -o $@

clean:
	$(RM) $(TARGET).svg