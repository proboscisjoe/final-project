FROM ubuntu:14.04
RUN sudo mkdir /lkm
COPY lkm.ko /lkm/
RUN sudo insmod /lkm/lkm.ko en0_ip_str=192.168.0.1
