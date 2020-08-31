
- remove AWS KEYs from environment variables and create an AMI with instance role instead
- have QA instance to be created from scratch (from the API) and terminated instead or stopped/restarted + use spot instance / fleet for the QA instance
- find better way to manage env variables


amzon linux 2 launch config with
- s3 role
- spot instance?

# amzon linux 2 setup:

## AMI baked:

#enable password for ansible to ssh?

sudo yum update -y

sudo yum install awscli python3 python3-pip make curl -y
sudo alias python='python3'
sudo alias pip='pip3'
sudo pip install docker docker-compose boto3 botocore


sudo amazon-linux-extras install docker -y
sudo service docker start
sudo service docker enable
sudo usermod -a -G docker ec2-user
sudo docker info

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version

docker login --username= --password=


## User data

aws s3 cp s3://portfoliogb/docker_deploy_tarballs/docker_deploy_app_demo_cd_pipeline.tar.gz .
tar -xvf docker_deploy_app_demo_cd_pipeline.tar.gz
cd docker_deploy_app_demo_cd_pipeline/deployment

mkdir docker-deployment/nginx/certs
aws s3 cp s3://portfoliogb/ssl_certs/cert_chain.crt ./docker-deployment/nginx/certs/
aws s3 cp s3://portfoliogb/ssl_certs/www_gbournique_com.key ./docker-deployment/nginx/certs/

export BUILD=dev
source .env
make up
make check-services-health


