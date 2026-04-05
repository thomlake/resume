SHORT=thomlake-resume-short
MEDIUM=thomlake-resume-medium
LONG=thomlake-resume-long

all: short medium long

short:
	python scripts/generate_pdf.py src/$(SHORT).md dist/$(SHORT).pdf

medium:
	python scripts/generate_pdf.py src/$(MEDIUM).md dist/$(MEDIUM).pdf

long:
	python scripts/generate_pdf.py src/$(LONG).md dist/$(LONG).pdf