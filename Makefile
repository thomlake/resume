SHORT=thomlake-resume-short
LONG=thomlake-resume-long

all: short long

short:
	python scripts/generate_pdf.py src/$(SHORT).md dist/$(SHORT).pdf

long:
	python scripts/generate_pdf.py src/$(LONG).md dist/$(LONG).pdf