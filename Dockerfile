# Use a imagem oficial do Python como base
FROM python:3.9

# Defina a variável de ambiente PYTHONUNBUFFERED para garantir que os logs do Python sejam enviados para o console
ENV PYTHONUNBUFFERED=1

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências usando pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

# Defina o comando para executar seu aplicativo
CMD ["python", "main.py"]
