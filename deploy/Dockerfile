# required environment variables:
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - HOSTED_ZONE_ID
# - RECORD_NAME
# - LOG_LOCATION

FROM python:3
WORKDIR /app

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# set up cron
RUN apt-get update
RUN apt-get -y install cron
RUN crontab -l | { cat; echo "PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin"; } | crontab -
RUN crontab -l | { cat; echo "LD_LIBRARY_PATH=/usr/local/lib"; } | crontab -
RUN crontab -l | { cat; echo "SHELL=/bin/bash"; } | crontab -
RUN crontab -l | { cat; echo "BASH_ENV=/container.env"; } | crontab -
RUN crontab -l | { cat; echo "*/5 * * * * python /app/main.py > /proc/1/fd/1 2>/proc/1/fd/2"; } | crontab -
COPY deploy/startup.sh .
RUN chmod +x /app/startup.sh

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# set up script
COPY main.py .

CMD ["bash", "/app/startup.sh"]
