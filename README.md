# Docket

pull and converge Dockerfiles into a single image via composition.
analogous to npm + package.json for docker

## usage

     pip install https://github.com/ack/docket/zipball/master
     docket merge dockerfile/redis local-directory > Dockerfile
     docker build -t rocket .
     docker run -rm -i -t rocket


local-directory/Dockerfile

      FROM dockerfile/ubuntu
      RUN apt-get install -qy supervisor
      # toplevel supervisor config
      ADD supervisord.conf /etc/supervisor/supervisord.conf



## features

- converges commands into supervisor configuration
- coalesces github/private repos, local directories, and curl-able resources

## why

an alternative to forking/hacking existing Dockerfiles:
compose/wrap them in a docket instead

## under the hood

docket simply parses/interprets your dockerfiles in sequence as passed
on the command line, culling certain entries and mutating others to
generate an aggregated Dockerfile. 


## dependencies

- python 2.6+
- git in PATH
