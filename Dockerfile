FROM toxchat/py-toxcore-c

RUN mkdir /opt/toxbot
WORKDIR /opt/toxbot
ADD ./src .
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENTRYPOINT [ "python", "setup.py" ]