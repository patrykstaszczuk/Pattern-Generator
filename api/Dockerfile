FROM python:3.9

WORKDIR /code

COPY ./api/requirements.txt /code/requirements.txt
COPY ./packages/PatternGenerator /packages/PatternGenerator

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api/app /code/app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
