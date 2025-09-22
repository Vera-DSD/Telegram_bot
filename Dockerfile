FROM python:3.10-slim

WORKDIR /app
ENV TOKEN='8187347038:AAEQzihWWE20WG4F77Zp3yw1bNE_f14no_w'
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
