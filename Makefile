install:
	poetry install --no-root

update-check:
	poetry show --outdated

update-test:
	poetry update --dry-run

update:
	poetry update
