RUN=poetry run

.PHONY: docs

build:
	$(RUN) poetry build

test:
	$(RUN) coverage run -m pytest tests/
	$(RUN) coverage report

docs:
	$(RUN) mkdocs serve

publish_docs:
	$(RUN) mkdocs gh-deploy

clean:
	rm -rf .pytest_cache site .coverage htmlcov dist
