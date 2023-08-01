FROM continuumio/miniconda3:latest

WORKDIR usr/src/pdf_pseudo_api

RUN apt-get update && apt-get install -y imagemagick

ADD environment.yml environment.yml

RUN conda env create -f environment.yml --force
ENV PATH /opt/conda/envs/pdf_pseudo_env/bin:$PATH
COPY . .