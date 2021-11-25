FROM python:3

WORKDIR /app

RUN pip install Flask
RUN pip install numpy
RUN pip install pandas
RUN pip install requests

COPY . .

RUN python api.py

CMD ["python", "app.py"]