FROM python:3.9

# Update aptitude with new repo
RUN apt-get update

# Install software 
RUN apt-get install -y git virtualenv

# Clone the files into the docker container
RUN git clone https://github.com/marcobaldanza/timesheet-jira-export.git

WORKDIR timesheet-jira-export

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install openpyxl

COPY config.conf .

ENTRYPOINT /usr/bin/python3 timesheet.py
