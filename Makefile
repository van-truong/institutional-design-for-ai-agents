SOURCE := ai4good_main.tex
PDF := icml2026-ai4good-camera-ready.pdf
BUILD_DIR := .build

.PHONY: pdf clean

pdf:
	mkdir -p $(BUILD_DIR)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=$(BUILD_DIR) $(SOURCE)
	cp $(BUILD_DIR)/ai4good_main.pdf $(PDF)

clean:
	latexmk -C -outdir=$(BUILD_DIR) $(SOURCE)
	rm -rf $(BUILD_DIR)

