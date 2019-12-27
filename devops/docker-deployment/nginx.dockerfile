FROM nginx:1.17-alpine

# Clean up existing nginx configs
RUN rm /etc/nginx/conf.d/default.conf

# Copy new config file
COPY devops/docker-deployment/config/django.conf /etc/nginx/conf.d/