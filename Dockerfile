# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/raspberrypi3-python:2.7
# Set working directory
WORKDIR /usr/src/app

# Install dependencies
RUN    apt-get update \
    && apt-get install -yq ccache 

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
#RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN pip install -r /requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY . ./

# Copy the networking file into place
COPY 

# Install dronology GCS
RUN git config --global user.name "dronology-outdoor" &&\
git config --global user.email dronology-outdoor@nonsense.com
git clone https://github.com/SAREC-Lab/Dronology-GCS.git

# main.py will run when container starts up on the device
CMD ["python","src/main.py"]
