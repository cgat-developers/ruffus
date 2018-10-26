# run all tests in paralell
#
# use the variable PYTEST_OPTIONS to configure pytest, for example:
#
#    make all PYTEST_OPTIONS="-v --lf"
#
SHELL=/bin/bash

PYTEST_OPTIONS?=-v

PYTEST=$(wildcard test_*.py)
NOTEST=$(wildcard check_*.py)

PYTEST_RUN=$(PYTEST:%.py=%.pytest)
NOTEST_RUN=$(NOTEST:%.py=%.run)

all: $(PYTEST_RUN) $(NOTEST_RUN)

%.pytest: %.py
	pytest $(PYTEST_OPTIONS) $<

%.run: %.py
	python $<
