FROM ubuntu:14.04
RUN sudo mkdir /lkm
COPY lkm.ko /lkm/
RUN sudo insmod /lkm/lkm.ko
