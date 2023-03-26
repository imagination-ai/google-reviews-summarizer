FROM python:3.11
#docker pull python:3.11

# Create the directories
RUN mkdir -p /build/test
RUN mkdir /applications

# Copy the necessary files to build and install these needed packages
COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt

COPY requirements-test.txt /build/requirements-test.txt
RUN pip3 install -r /build/requirements-test.txt

COPY requirements-dev.txt /build/requirements-dev.txt
RUN pip3 install -r /build/requirements-dev.txt

# Add related Python utility tools
COPY .isort.cfg /build/.isort.cfg
COPY pytest.ini /build/pytest.ini
COPY .flake8 /build/.flake8

# Define environment variables
ENV APP_RESOURCE_DIR /applications
ENV PYTHONPATH /applications

##### 1. Leaf Image: summarizer #####
COPY summarizer /applications/summarizer
COPY summarizer-resources /applications/summarizer-resources

# Make port 8080 available to the world outside this container
EXPOSE 8080
