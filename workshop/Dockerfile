
FROM python:3.6

COPY . /app

RUN pip3 install -r /app/models/requirements.txt
RUN chmod 777 -R /app

ENV DATA_PATH /app/models/kc_house_data.csv
ENV TRAINED_MODEL_PATH /trained-model-file

CMD python3 /app/test.py
