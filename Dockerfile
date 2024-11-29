FROM python:3.9

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY req.txt .

RUN pip install  --no-cache-dir --upgrade -r req.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--port", "80"]