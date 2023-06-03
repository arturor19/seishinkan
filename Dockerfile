FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR ./foliounico/
COPY requirements.txt ./foliounico/
RUN pip install -r ./foliounico/requirements.txt
RUN apt-get update && apt-get install -y \
gettext \
#COPY . /code/
