# Makefile

.PHONY: render
render:
	python resume/generator.py

.PHONY: clean
clean:
	rm -rf outputs/pdf/*.out 
	rm -rf outputs/pdf/*.log
	rm -rf outputs/pdf/*.aux
	find . -name "__pycache__" -type d -exec rm -rf {} +

.PHONY: compare
compare:
	python src/scripts/run_compare_pdf.py