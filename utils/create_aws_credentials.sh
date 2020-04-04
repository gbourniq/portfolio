#!/usr/bin/env bash

mkdir -p ~/.aws

cat > ~/.aws/credentials << EOL
[default]
aws_access_key_id = AKIAVIFROS5RZ4VHRCYS
aws_secret_access_key = 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
EOL

cat > ~/.aws/config << EOL
[profile default]
region = eu-west-2
output = json
EOL

