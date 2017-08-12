# Docker Util

[SaltStack](https://github.com/saltstack/salt) Version 2017.7.14

The Docker Util module allows you to manage Docker swarm clusters via [SaltStack](https://github.com/saltstack/salt)

**CodeAuthor** Tyler Jones <tylerjones4508@gmail.com>

## About

This is designed to be used with [SaltStack](https://github.com/saltstack/salt) modules. For more information about how to configure your custom Salt modules visit [This     Link](https://docs.saltstack.com/en/latest/ref/modules/#writing-execution-modules). The [SaltStack](https://github.com/saltstack/salt) State modules will follow at a later date.

## REQUIREMENTS:


docker-sdk can be installed via pip and it is required to work with [SaltStack](https://github.com/saltstack/salt):

```bash
pip install -U docker
```

## Docker Swarm Salt Module

### The following will create a Docker Swarm Manager

###docker_util.swarm_init(advertise_addr=str,listen_addr=int, force_new_cluster=bool )


```bash
salt <target> docker_util.swarm_init advertise_addr='ens4' listen_addr='0.0.0.0' force_new_cluster=False
```

```yaml
Comment:
    Docker swarm has been Initalized on Salt-Master and the worker/manager Join token is below
Manger_Token:
    SWMTKN-1-1yv40emizau5b1hy2x3boj3vcsy7edoldjxooif13kx9jpv97e-4jakordba7mvirp0a8vw4ib7v
Worker_Token:
    SWMTKN-1-1yv40emizau5b1hy2x3boj3vcsy7edoldjxooif13kx9jpv97e-ec78dxpr06sfhplqr05nncihn
```



### The following will join a minion to a Docker Swarm

**Join a Swarm as a worker or manager.**

###docker_util.joinswarm(remote_addr, listen_addr, token)

**Note** You have to pass in the token


```bash
salt <target> docker_util.joinswarm 10.1.0.2 0.0.0.0 SWMTKN-1-1yv40emizau5b1hy2x3boj3vcsy7edoldjxooif13kx9jpv97e-ec78dxpr06sfhplqr05nncihn
```


```yaml
Comment:
   instance-1-minion.c.optimum-tensor-161912.internal has joined the Swarm
Worker/ManagerIP:
   10.1.0.3
```

#### The following will leave a Docker Swarm



###docker_util.leave_swarm(force=bool)




## Docker Services Salt Module

### docker_util.service_create(image=str,name=str,command=str,hostname=str,replicas=int,target_port=int,published_port=int)



**Note: You have to have a swarm running for this to work**

Here we are going to create a docker service with salt on the targeted minion.
