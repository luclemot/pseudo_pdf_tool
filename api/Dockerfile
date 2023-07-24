FROM continuumio/miniconda3:latest

WORKDIR usr/src/pdf_pseudo_api

ADD environment.yml environment.yml

RUN conda env create -f environment.yml --force
RUN conda install fastapi uvicorn
ENV PATH /opt/conda/envs/pseudo_pdf_env/bin:$PATH
COPY . .