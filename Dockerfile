FROM python:latest

RUN apt-get update && apt-get install -y

#RUN apt-get install -y

#Customize .bashrc
RUN curl -o /root/.bashrc https://gist.githubusercontent.com/Unitato/b81a4b974beb5ec9500014fa67dc4946/raw/91a44645e6768a2c5cfbdfcea9c56176ac212b4e/.bashrc

WORKDIR /app

#install gitsecrets
RUN git clone https://github.com/awslabs/git-secrets && cd git-secrets && make install && git secrets --install -f

COPY src/requirements.txt ./
RUN pip install -r /app/requirements.txt

COPY config ./config/
COPY src ./

CMD bash
