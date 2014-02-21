# Pull base image.
FROM ubuntu:12.10

# Update OS.
RUN echo "deb http://archive.ubuntu.com/ubuntu quantal main universe multiverse" > /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y

# Install basic packages.
RUN apt-get install -y software-properties-common
RUN apt-get install -y curl git htop unzip vim wget

# Add files.
ADD root/bashrc /root/.bashrc

# Set working directory.
ENV HOME /root
WORKDIR /root

EXPOSE 80 512
VOLUME /tmp

CMD ["python", "-V"]