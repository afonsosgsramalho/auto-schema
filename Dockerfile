FROM python:3.12-slim

WORKDIR /autoschema

COPY . /autoschema

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "autoschema/"]