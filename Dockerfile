# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/raspberrypi3-python:latest
ENV COMMIT=99a4a7b4ac7329e015738bbcb99c5883d45436d6

# Set working directory
WORKDIR /usr/src/app

#TODO Commented out for now to save time, remove comments for deployment
## Update and Install dependencies
RUN    apt-get update \
    && apt-get install -yq ccache wireless-tools dbus 
RUN export  DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt
COPY ./AIR1 /AIR1
# Install python modules
#TODO Switch commented out lines to include upgrading
RUN pip install --upgrade pip && pip install -r /requirements.txt
#RUN pip install -r /requirements.txt

## Clone repo and checkout latest commit to force updates
#RUN git clone https://github.com/dronology-outdoor/PiDronology.git /usr/src/app
#RUN git checkout -q $COMMIT	

# This will copy all files in our root to the working  directory in the container
COPY . ./

# Copy the networking file into place
#COPY ./DronologyAdHoc /system-connections/

# main.py will run when container starts up on the device
#CMD ["python","-u", "main.py", "--settings=resin_settings"]
CMD ["python", "/src/main.py"]
