FROM python:3.11-slim-bookworm

ENV DockerHOME=/home/app/webapp
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DockerHOME
RUN mkdir $DockerHOME/staticfiles
WORKDIR $DockerHOME

COPY requirements.txt $DockerHOME/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . $DockerHOME

# Add the user and grant necessary permissions
RUN adduser --disabled-password --gecos "" user
RUN chown -R user:user $DockerHOME
RUN chmod -R 755 $DockerHOME

USER user

EXPOSE 8000

ENTRYPOINT ["/home/app/webapp/entrypoint.sh"]
