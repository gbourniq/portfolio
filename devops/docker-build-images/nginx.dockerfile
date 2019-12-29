FROM nginx:1.17-alpine

# Clean up existing nginx configs
RUN rm /etc/nginx/conf.d/default.conf

# Copy new config file
COPY devops/docker-build-images/config/django.conf /etc/nginx/conf.d/django.conf