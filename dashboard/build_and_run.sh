docker build -t sli-grafana .

docker run \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
    -e AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} \
    -p 3000:3000 sli-grafana
