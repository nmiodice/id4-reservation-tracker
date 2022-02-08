FROM python:3.8

# update pip and other python dependencies
RUN python3 -m pip install --upgrade pip setuptools wheel

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/



# install python app
WORKDIR /src
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY *.py ./

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
CMD ["python3", "main.py"]
