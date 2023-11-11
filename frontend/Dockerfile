FROM nginx:1.25

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d


WORKDIR /app

COPY ./public/ .
CMD ["nginx", "-g", "daemon off;"]
