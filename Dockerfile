# image with GPU support
FROM pytorch/pytorch:latest

RUN mkdir -p /app/util_data/

COPY app.py /app/
COPY requirements.txt /app/
COPY util_data/list_names_cat.csv /app/util_data/
COPY templates/ /app/templates/

WORKDIR /app

RUN apt-get update && apt-get install -y tesseract-ocr libgl1-mesa-glx
RUN pip install -r requirements.txt
# spaCy models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download es_core_news_sm
RUN python -m spacy download ca_core_news_sm

EXPOSE 5000

CMD ["python", "app.py"]
