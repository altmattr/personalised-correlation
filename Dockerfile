FROM python:3

WORKDIR /app

RUN pip install --user Flask
RUN pip install --user numpy
RUN pip install --user pandas
RUN pip install --user requests

COPY . .

CMD ["python", "app.py"]