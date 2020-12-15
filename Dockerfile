#########################################
# Dockerfile for BAE Activation Service #
#########################################
FROM python:3-onbuild

# User
RUN groupadd --gid 5000 aservice \
    && useradd --home-dir /home/aservice --create-home --uid 5000 \
        --gid 5000 --shell /bin/sh --skel /dev/null aservice
COPY . /home/aservice
USER aservice
WORKDIR /home/aservice

# requirements
RUN pip3 install -r requirements.txt

# Start gunicorn
EXPOSE 5000
CMD ["gunicorn", "--log-file=-", "-b", "0.0.0.0:5000", "-w", "4", "wsgi:app"]
