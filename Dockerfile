# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/raspberrypi3-python:latest
# Set working directory
WORKDIR /usr/src/app

#TODO Commented out for now to save time, remove comments for deployment
## Update and Install dependencies
#RUN    apt-get update \
#    && apt-get install -yq ccache 

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# Install python modules
#TODO Switch commented out lines to include upgrading
#RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN pip install -r /requirements.txt

# Cone repo
RUN git clone https://github.com/dronology-outdoor/PiDronology.git 	

# This will copy all files in our root to the working  directory in the container
COPY . ./

# Copy the networking file into place
#COPY ./DronologyAdHoc /system-connections/

# main.py will run when container starts up on the device
#CMD ["python","--version"]
#CMD ["python", "src/main.py"]
#CMD ["python","-u", "src/main.py", "--settings=resin_settings"]
CMD ["python","-u", "PiDronology/main.py", "--settings=resin_settings"]
