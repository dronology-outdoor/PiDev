# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/raspberrypi3-python:3
# Set working directory
WORKDIR /usr/src/app

# Install dependencies
RUN    apt-get update \
    && apt-get install -yq 
#        g++ \
#        python3-dev \
#        python3-pip \
#        python3-setuptools \
#        python3-wheel \
#        python3-numpy \
#        python3-scipy

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
#RUN pip install --upgrade pip && pip install -r /requirements.txt
#RUN pip3 install -r /requirements.txt
RUN pip --version

# This will copy all files in our root to the working  directory in the container
COPY . ./

# main.py will run when container starts up on the device
CMD ["python","src/main.py"]
