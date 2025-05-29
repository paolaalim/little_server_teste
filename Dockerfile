# Usa uma imagem oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para o container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta que a aplicação usará
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
