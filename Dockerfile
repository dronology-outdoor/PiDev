# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/raspberrypi3-python:3

# Set our working directory
WORKDIR /usr/src/app

# Config and INSTALLS
## 1. INSTALL Dronology
RUN apt-get update && apt-get install -yq ccache && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN cd $WORKDIR
#    git clone <> && \
#    cd Dronology-GCS && \
#    git checkout integration

## 2 Install dependancies
RUN wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh &&\
bash Miniconda3-latest-Linux-armv7l.sh -b &&\
python --version
## 2. Stop trying to use a synced timeserver - assume no internet connection
#RUN systemctl stop systemd-timesyncd

## 3. TODO setup resinOS version of ssh

## 4. INSTALL and run test application 
###Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

##5.  pip install python deps from requirements.txt on the resin.io build server
RUN pip install --upgrade pip && pip install -r /requirements.txt


##6. This will copy all files in our root to the working  directory in the container
COPY . ./

##7. switch on systemd init system in container
ENV INITSYSTEM on

# Run Applications
### main.py will run when container starts up on the device
CMD ["python","-u","src/main.py","--settings=resin_settings"]
#CMD ["python","-u","src/main.py"]
