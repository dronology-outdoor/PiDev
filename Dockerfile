# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/raspberrypi3-python:latest
ENV COMMIT=c5a8d537ead19dfac9ac1a09ea834809e3bdb886
ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
# Set working directory
WORKDIR /usr/src/app

#TODO Commented out for now to save time, remove comments for deployment
## Update and Install dependencies
###RUN    apt-get update \
###    && apt-get install -yq ccache wireless-tools dbus 

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# Install python modules
#TODO Switch commented out lines to include upgrading
##RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN pip install -r /requirements.txt


# Clone Onboard dronology repo and checkout latest commit to force updates
RUN git clone https://github.com/dronology-outdoor/PiDronology.git /usr/src/app
RUN git checkout -q $COMMIT	

# This will copy all files in our root to the working  directory in the container
COPY . ./

#Run main.py to configure adhoc network
#CMD ["python","-u", "src/main.py", "--settings=adhoc_network"]
# main.py will run when container starts up on the device
#CMD ["python","-u", "app/main.py", "--settings=dronology_Settings"]
CMD ["bash", "start.sh"]
