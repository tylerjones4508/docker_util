Salty Docker
------------
..versionadded: 2017.7.14

The Salty Docker module allows you to manage Docker swarm clusters via **Salt Stack**

:codeauthor Tyler Jones <tylerjones4508@gmail.com>


About
-----

This is designed to be used with **Salt Stack** modules. Salt State modules will follow at a later date.

REQUIREMENTS:
------------

docker-sdk can be installed via pip:

..code-block::bash

    pip install docker


Docker Swarm Salt Module
------------------------
**Docker Swarm Init**

The following will create a docker swarm manager


..code-block::bash

    salt minion salty_docker.swarm_init advertise_addr='ens4' listen_addr='0.0.0.0' force_new_cluster=False


..code-block::bash

    Comment:
        Docker swarm has been Initalized on Salt-Master and the worker/manager Join token is below
    Manger_Token:
        SWMTKN-1-1yv40emizau5b1hy2x3boj3vcsy7edoldjxooif13kx9jpv97e-4jakordba7mvirp0a8vw4ib7v
    Worker_Token:
        SWMTKN-1-1yv40emizau5b1hy2x3boj3vcsy7edoldjxooif13kx9jpv97e-ec78dxpr06sfhplqr05nncihn
