SOURCE := lncs_main.tex
PDF := springer-lncs-proceedings.pdf
BUILD_DIR := .build

.PHONY: pdf figures clean

pdf: figures
	mkdir -p $(BUILD_DIR)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(BUILD_DIR) $(SOURCE)
	cp $(BUILD_DIR)/lncs_main.pdf $(PDF)

figures:
	./render_figures.sh

clean:
	latexmk -C -outdir=$(BUILD_DIR) $(SOURCE)
	rm -rf $(BUILD_DIR)
