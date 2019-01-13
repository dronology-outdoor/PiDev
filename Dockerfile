# base-image for python on any machine using a template variable,
FROM balenalib/raspberrypi3-debian-python:latest
ENV COMMIT=c5a8d537ead19dfac9ac1a09ea834809e3bdb886
ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
# Set working directory
WORKDIR /usr/src/app

#TODO Commented out for now to save time, remove comments for deployment
## Update and Install dependencies
RUN install_packages git
RUN    apt-get update \
    && apt-get install -yq dbus gcc 

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# Install python modules
#TODO Switch commented out lines to include upgrading
##RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN pip install -r /requirements.txt


# Clone Onboard dronology repo and checkout latest commit to force updates
WORKDIR /usr/src/app/application
RUN touch mzansi0
RUN git clone https://github.com/dronology-outdoor/PiDronology.git
RUN touch mzansi1
RUN ls
RUN ls PiDronology/
#RUN git checkout -q $COMMIT	
#COPY PiDronology/requirements.txt /requirements.txt
RUN touch mzansi2
RUN pip install -r PiDronology/requirements.txt
#RUN touch mzansi3
#RUN pip install -r PiDronology/requirements.txt

WORKDIR /usr/src/app
# This will copy all files in our root to the working  directory in the container
COPY . ./
RUN touch mzansi4
CMD ["bash", "start.sh"]
