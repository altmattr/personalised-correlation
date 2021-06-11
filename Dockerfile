FROM python:3

WORKDIR /app

RUN pip install Flask
RUN pip install numpy
RUN pip install pandas
RUN pip install requests

COPY . .

CMD ["python", "app.py"]