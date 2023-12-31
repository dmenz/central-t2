FROM nginx:1.25

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD python3 manage.py collectstatic --noinput \
    && python3 manage.py migrate \
    && service nginx start \
    && gunicorn backend.wsgi --bind 0.0.0.0:1337
