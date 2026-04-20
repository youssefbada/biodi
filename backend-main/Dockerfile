FROM nexus.retd.edf.fr/python:3.13-slim


WORKDIR /app

COPY requirements.txt requirements.txt


# RUN pip install --no-cache-dir -r requirements.txt
# Configurer pip pour passer par le mirror Nexus EDF
RUN pip install --no-cache-dir \
    --index-url https://nexus.retd.edf.fr/repository/pypi-proxy/simple/ \
    --trusted-host nexus.retd.edf.fr \
    -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "120", "config.wsgi:application"]
