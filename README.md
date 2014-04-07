# Docket

Pull and converge Dockerfiles into a single image via composition.
Interprets/aggregates intermediary container definitions into a single
buildable Dockerfile as a marginally better alternative to fork/hack.

Version control, audit, and salt the bits in your single-vm containers.

In tandem with [espb](https://github.com/ack/espb) build yourself a
composable/decomposable stack from Dockerfile building blocks.


## features


* converges commands into supervisor configuration
* coalesces github/private repos, local directories, and curl-able resources
* optionally injects a service discovery agent for inter-container coordination




## usage

    $ pip install https://github.com/CenturyLinkLabs/docket/zipball/master

    $ docket -h
    Usage: docket [options] <command> [args]

    Dockerfile wrapping paper
    supported commands:

      generate - create a new Docketfile to bind entire container together
         arg1: project name (creates library/<name>/Dockerfile etc)
         arg2: ancestor Dockerfile (should be shared across all merged Dockerfiles)

      merge - merge collapsed Dockerfiles
         args: (multiple) paths/refs to Dockerfiles



### generate

     $ docket generate awesome-stack dockerfile/ubuntu
     $ cat library/awesome-stack/Dockerfile
     <supervisord and wrapper injection>
     $ docker merge library/awesome-stack > Dockerfile

### merge

    $ docket merge dockerfile/redis local-directory > Dockerfile

    $ cat local-directory/Dockerfile
    FROM dockerfile/ubuntu
    RUN apt-get install -qy supervisor
    # toplevel supervisor config
    ADD supervisord.conf /etc/supervisor/supervisord.conf

    $ docker build -t rocket .
    <docker builder output>

    $ docker run -rm -i -t rocket

## under the hood

Docket simply parses/interprets your dockerfiles in sequence as passed
on the command line, culling certain entries and mutating others to
generate an aggregated Dockerfile. Generated and referenced Dockerfiles
are cached into a local `library` directory.

## dependencies

- python 2.6+
- git in PATH
