FROM ubuntu
RUN apt-get update && yes|apt-get upgrade
RUN apt-get install -y wget bzip2

# Anaconda installing
RUN wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
RUN bash Anaconda3-5.0.1-Linux-x86_64.sh -b
RUN rm Anaconda3-5.0.1-Linux-x86_64.sh
# Set path to conda
ENV PATH /root/anaconda3/bin:$PATH
# Updating Anaconda packages
RUN conda update conda
RUN conda update anaconda
RUN conda update --all

RUN conda install tensorflow
RUN conda install keras
RUN conda install --channel https://conda.anaconda.org/menpo opencv3
RUN yes|apt-get install libgtk2.0-0
RUN conda install -c anaconda flask-cors

RUN mkdir /app/ /app/resources /app/saved_models
WORKDIR /app/

COPY saved_models/ /app/saved_models/
COPY web_starter.py /app/

CMD ["python3", "web_starter.py"]