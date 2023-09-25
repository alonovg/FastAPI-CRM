FROM python:3.9

RUN mkdir /crm

WORKDIR /crm

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /crm/docker/*.sh

#CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]