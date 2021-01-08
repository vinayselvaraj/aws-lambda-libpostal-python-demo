FROM public.ecr.aws/lambda/python:3.8

RUN yum groupinstall "Development Tools" -y

RUN mkdir /build
RUN cd /build && git clone https://github.com/openvenues/libpostal
RUN mkdir -p /data/libpostal
RUN cd /build/libpostal && ./bootstrap.sh
RUN cd /build/libpostal && ./configure --datadir=/data/libpostal
RUN cd /build/libpostal && make -j5 && make install
RUN ln -s `ls /usr/local/lib/libpostal.so.1.*` /usr/lib/libpostal.so.1
RUN ln -s `ls /usr/local/lib/libpostal.so.1.*` /usr/lib/libpostal.so
RUN ln -s `ls /usr/local/lib/libpostal.so.1.*` /usr/lib64/libpostal.so.1
RUN ln -s `ls /usr/local/lib/libpostal.so.1.*` /usr/lib64/libpostal.so

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY lambda/* ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]