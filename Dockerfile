FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR ./foliounico/
COPY requirements.txt ./foliounico/
RUN pip install -r ./foliounico/requirements.txt
RUN apt-get update && apt-get install -y \
gettext \
#COPY . /code/
