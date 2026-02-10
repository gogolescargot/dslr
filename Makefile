SHELL := /bin/bash
PY := python3
VENV := venv
PYBIN := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: all venv requirements clean fclean re lint

all: lint venv requirements
	@echo 'To activate the virtual environment, run: source $(VENV)/bin/activate'

lint:
	@echo "Running flake8..."
	@$(PYBIN) -m flake8 --exclude=$(VENV); rc=$$?; \
	if [ $$rc -eq 0 ]; then \
			echo "No issues"; \
	fi; \
	true
	@echo

venv:
	@echo "Checking for virtual environment..."
	@if [ ! -d "$(VENV)" ]; then \
			$(PY) -m venv $(VENV); \
			echo "Virtual environnement created in $(VENV)"; \
	else \
			echo "Virtual environment already exists"; \
	fi
	@echo

requirements: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo

describe:
	@echo "Describing dataset..."
	$(PYBIN) src/describe.py
	@echo

histogram:
	@echo "Generating histogram..."
	$(PYBIN) src/histogram.py
	@echo

scatterplot:
	@echo "Generating scatter plot..."
	$(PYBIN) src/scatter_plot.py
	@echo

pairplot:
	@echo "Generating pair plot..."
	$(PYBIN) src/pair_plot.py
	@echo

train:
	@echo "Training model..."
	$(PYBIN) src/logreg_train.py
	@echo

predict:
	@echo "Predicting with model..."
	$(PYBIN) src/logreg_predict.py
	@echo

clean:
	@echo "Cleaning up..."
	-rm -f houses.csv weights.pkl
	-find . -type d -name __pycache__ -exec rm -rf {} +
	@echo

fclean: clean
	@echo "Removing virtual environment..."
	-rm -rf $(VENV)
	@echo

re: fclean all