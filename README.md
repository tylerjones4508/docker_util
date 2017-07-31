Salty Docker
------------
..versionadded: 2017.7.14

The Salty Docker module allows you to manage Docker swarm clusters via Salt Stack

:codeauthor Tyler Jones <tylerjones4508@gmail.com>

REQUIREMENTS:

docker-sdk can be installed via pip:

..code-block::bash

    pip install docker

Salty Docker Examples:
----------------------

*docker swarm init

..code-block::bash

    salt minion salty_docker.swarm_init advertise_addr='ens4' listen_addr='0.0.0.0' force_new_cluster=False


..code-block::bash

    test
