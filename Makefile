serve:
	docker run --rm -it -p 8000:8000 -v ${PWD}:/docs -w /docs python:3.13-slim sh -c "pip install -q -r requirements.txt && mkdocs serve -a 0.0.0.0:8000"
