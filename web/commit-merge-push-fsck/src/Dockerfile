FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY . /usr/share/nginx/html

RUN mv /usr/share/nginx/html/[dot]git /usr/share/nginx/html/.git
RUN rm /usr/share/nginx/html/nginx.conf

EXPOSE 80
