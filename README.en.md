# CGI+WebServer

## Introduction

    CGI of Beijing University of Technology, multithreaded WebServer job

## Document structure

    Webroot root

    Webroot/src network server

    Webroot/cgi bin CGI program

    webroot/css css

    Webroot/picture picture

    Webroot/html static webpage

    Webroot/log log

## Environment installation

    Use pip for virtual environment management. Please pre install python 3.8.10 or use other package managers

    git clone https://github.com/zhixiaoni/CGI-WebServer.git

    python -m venv webroot

    webroot/.venv/Scripts/activate

    (.venv) pip install -r webroot/requirements.txt

## Instructions

    Run directly

    (.venv) python webroot/src/main. py -p xxxx --ip x.x.x.x -maxc x -maxw x

    Parameter default values: port 8888, ip 127.0.0.1, maxc max connection 8, maxw max wait 16

    The log is in the log directory