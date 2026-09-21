.PHONY: pdf figures clean

pdf:
	$(MAKE) -C manuscript pdf

figures:
	$(MAKE) -C manuscript figures

clean:
	$(MAKE) -C manuscript clean
