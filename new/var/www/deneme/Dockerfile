FROM python:3.6-alpine
RUN apk --update add bash nano
COPY ./requirements.txt .
COPY ./flask_app.py .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "flask_app.py"]
