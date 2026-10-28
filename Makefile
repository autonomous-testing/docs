serve:
	docker run --rm -it -p 8000:8000 -v ${PWD}:/docs -w /docs python:3.13-slim sh -c "pip install -q -r requirements.txt && zensical serve -a 0.0.0.0:8000"

check:
	docker run --rm -v ${PWD}:/docs -w /docs python:3.13-slim sh -c "pip install -q -r requirements.txt && python scripts/check-media.py && zensical build --strict"
