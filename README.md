# Docker Util

[SaltStack](https://github.com/saltstack/salt) Version 2017.7.14

The Docker Util module allows you to manage Docker swarm clusters via [SaltStack](https://github.com/saltstack/salt)

**CodeAuthor** Tyler Jones <tylerjones4508@gmail.com>

## About

This is designed to be used with [SaltStack](https://github.com/saltstack/salt) modules. For more information about how to configure your custom Salt modules visit [This     Link](https://docs.saltstack.com/en/latest/ref/modules/#writing-execution-modules). The [SaltStack](https://github.com/saltstack/salt) State modules will follow at a later date.

## REQUIREMENTS:

### SaltStack

To install [SaltStack](https://github.com/saltstack/salt) please visit https://repo.saltstack.com/.


### Docker Python Library

Docker Python [Libary](https://pypi.python.org/pypi/docker/) can be installed via pip and it is required to work with [SaltStack](https://github.com/saltstack/salt):

```bash
pip install -U docker
```
### Docker Installed on Minion/Masters

https://docs.docker.com/engine/installation/linux/docker-ce


## Docker Swarm Salt Module

### The following will create a Docker Swarm Manager

##### docker_util.swarm_init(advertise_addr=str,listen_addr=int, force_new_cluster=True/False )

```bash
salt 'saltmaster' docker_util.swarm_init advertise_addr='192.168.50.10' listen_addr='0.0.0.0' force_new_cluster=False
```

**Return Data**

```yaml
saltmaster:
    ----------
    Comment:
        Docker swarm has been Initalized on saltmaster and the worker/manager Join token is below
    Tokens:
        ----------
        Manager:
            SWMTKN-1-64tux2g0701r84ofq93zppcih0pe081akq45owe9ts61f30x4t-06trjugdu7x2z47j938s54ilh
        Worker:
            SWMTKN-1-64tux2g0701r84ofq93zppcih0pe081akq45owe9ts61f30x4t-9b7lviz7pj17jd1bk0k54dehc
```


### Show Join Tokens on swarm manager

#### docker_util.swarm_tokens

```bash
salt 'saltmaster' docker_util.swarm_tokens
```

**Return Data**

```yaml
saltmaster:
    ----------
    Manager:
        SWMTKN-1-64tux2g0701r84ofq93zppcih0pe081akq45owe9ts61f30x4t-06trjugdu7x2z47j938s54ilh
    Worker:
        SWMTKN-1-64tux2g0701r84ofq93zppcih0pe081akq45owe9ts61f30x4t-9b7lviz7pj17jd1bk0k54dehc
```

### The following will join a minion or master to a Docker Swarm

**Join a Swarm as a worker or manager.**

##### docker_util.joinswarm(remote_addr=int,listen_addr=int,token=str)

**Note** You have to pass in the token


```bash
salt 'minion1' docker_util.joinswarm remote_addr=192.168.50.10 listen_addr='0.0.0.0' token='SWMTKN-1-64tux2g0701r84ofq93zppcih0pe081akq45owe9ts61f30x4t-06trjugdu7x2z47j938s54il'
```

**Return Data**

```yaml
minion1:
    ----------
    Comment:
        minion1 has joined the Swarm
    Manager_Addr:
        192.168.50.10
```


