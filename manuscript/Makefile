SOURCE := manuscript.tex
PDF := ../manuscript.pdf
BUILD_DIR := .build

.PHONY: pdf figures clean

pdf:
	mkdir -p $(BUILD_DIR)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(BUILD_DIR) $(SOURCE)
	cp $(BUILD_DIR)/manuscript.pdf $(PDF)
	@# keep the tracked .bbl next to the source in sync: LaTeX reads ./manuscript.bbl before the build copy
	cp $(BUILD_DIR)/manuscript.bbl manuscript.bbl

figures:
	./render_figures.sh

clean:
	latexmk -C -outdir=$(BUILD_DIR) $(SOURCE)
	rm -rf $(BUILD_DIR)
