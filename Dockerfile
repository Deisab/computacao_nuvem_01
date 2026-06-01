# Usa a imagem oficial do Python, que é a recomendação para aplicações Python
FROM python:3.10-slim

# Define o diretório de trabalho padrão
WORKDIR /app

# Copia apenas os arquivos de dependência primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências listadas
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o seu código fonte para o diretório de trabalho
COPY . .

# Expõe a porta que o FastAPI utiliza (padrão 8000)
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
# Certifique-se que seu main.py tenha o objeto 'app' definido
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
