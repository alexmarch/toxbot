FROM toxchat/py-toxcore-c

RUN mkdir /opt/toxbot
WORKDIR /opt/toxbot
RUN mkdir logs
RUN mkdir ids
ADD ./src/bot .
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENTRYPOINT [ "python", "setup.py" ]