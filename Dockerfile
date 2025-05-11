FROM python:3.9-slim

WORKDIR /app

# Copia i file necessari
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta su cui gira l'applicazione
EXPOSE 5000

# Comando per avviare l'applicazione
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]