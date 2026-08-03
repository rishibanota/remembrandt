.PHONY: install test demo demo-reset push-readme

install:
	bash scripts/install.sh

test:
	python -m pytest -q

demo:
	rm -rf .remembrandt
	python -m agent_memory remember "Use uv for dependency management" --category decision --tags uv
	python -m agent_memory remember "Never mutate the shared config object" --category gotcha
	python -m agent_memory remember "Added /api/health endpoint" --category changelog
	python -m agent_memory recall
	python -m agent_memory resume

# Recreate the demo memory shown in the README inside examples/demo
demo-data:
	rm -rf examples/demo/.remembrandt
	cd examples/demo && \
	python -m agent_memory --dir .remembrandt remember "Use uv for dependency management" --category decision --tags uv && \
	python -m agent_memory --dir .remembrandt remember "Never mutate the shared config object" --category gotcha && \
	python -m agent_memory --dir .remembrandt remember "Refactor auth to JWT" --category changelog && \
	python -m agent_memory --dir .remembrandt resume

demo-reset:
	rm -rf .remembrandt examples/demo/.remembrandt
	@echo "Demo memory cleared."
