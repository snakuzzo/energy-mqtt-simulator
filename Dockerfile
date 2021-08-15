FROM python:alpine
COPY ./app/ /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./energy_simulator.py