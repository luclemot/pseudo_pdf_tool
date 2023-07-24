FROM continuumio/miniconda3:latest

WORKDIR usr/src/pdf_pseudo_api

ADD environment.yml environment.yml

RUN conda env create -f environment.yml
ENV PATH /opt/conda/envs/pseudo_pdf_env/bin:$PATH
RUN /bin/bash -c "source activate pseudo_pdf_env"
COPY . .