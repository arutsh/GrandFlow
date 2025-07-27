FROM python:3.13

WORKDIR /app

COPY services/users/requirements.txt .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
