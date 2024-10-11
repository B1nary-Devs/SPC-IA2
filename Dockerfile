# Use uma imagem base Python
FROM python:3.9

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto
COPY . .

# Instale as dependências
RUN pip install -r requirements.txt

# Exponha a porta em que a IA estará ouvindo
EXPOSE 8000

# Comando para iniciar a IA
CMD ["python", "model.py"]