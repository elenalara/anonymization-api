# Utiliza la imagen base de PyTorch con soporte de GPU
FROM pytorch/pytorch:latest

# Crear la carpeta 'util_data'
RUN mkdir -p /app/util_data/

# Copiar los archivos a la imagen de trabajo
COPY app.py /app/
COPY requirements.txt /app/
COPY util_data/list_names_cat.csv /app/util_data/
COPY templates/ /app/templates/

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y tesseract-ocr libgl1-mesa-glx
RUN pip install -r requirements.txt
# Instalar los modelos de spaCy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download es_core_news_sm
RUN python -m spacy download ca_core_news_sm

EXPOSE 5000

# Ejecutar el script
CMD ["python", "app.py"]
