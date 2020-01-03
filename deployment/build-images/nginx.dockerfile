FROM nginx:1.17-alpine

# Clean up existing nginx configs
RUN rm /etc/nginx/conf.d/default.conf

# Install curl dependency for healthcheck
RUN apk update \
    && apk add --no-cache curl

# Copy new config file
COPY deployment/build-images/config/nginx.conf /etc/nginx/conf.d/nginx.conf