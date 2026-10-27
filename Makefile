# Makefile for SHADOW-ML & Shadow Arena

PYTHON = .venv/Scripts/python.exe
PIP = .venv/Scripts/pip.exe
PYTEST = .venv/Scripts/pytest.exe
STREAMLIT = .venv/Scripts/streamlit.exe
UVICORN = .venv/Scripts/uvicorn.exe

.PHONY: setup dev streamlit test test-backend test-all deck gram clean

setup:
	python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

streamlit:
	$(STREAMLIT) run app.py

dev:
	$(UVICORN) backend.app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	$(PYTEST) -v tests

test-backend:
	$(PYTEST) -v backend/tests

test-all:
	$(PYTEST) -v tests backend/tests

slides:
	py scripts/build_html_slides.py

book:
	py scripts/build_master_book.py

deck:
	py scripts/build_comprehensive_deck.py

gram:
	$(PYTHON) scripts/demo_gram_matrix_vif.py

clean:
	powershell -Command "Get-ChildItem -Directory -Exclude .venv | ForEach-Object { Get-ChildItem -Path $$($$_.FullName) -Include '__pycache__','.pytest_cache' -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue }"


