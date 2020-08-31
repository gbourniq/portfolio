# Instructions

For a fresh deployment, please follow the below instructions.


1. Run one of the following command:
- `export BUILD=prod` to use nginx (production deployment) 
- `export BUILD=dev` to NOT use nginx (dev, qa deployment)

2. (Optional) If prod deployment, download the SSL certificate and private key
```
mkdir docker-deployment/nginx/certs
sudo aws s3 cp s3://portfoliogb/ssl_certs/cert_chain.crt ./docker-deployment/nginx/certs/
sudo aws s3 cp s3://portfoliogb/ssl_certs/www_gbournique_com.key ./docker-deployment/nginx/certs/
```

3. Source environment variables and deploy app
```
source .env
make up
make check-services-health
```

