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





## Docker Swarm Salt Module

### The following will create a Docker Swarm Manager

##### docker_util.swarm_init(advertise_addr=str,listen_addr=int, force_new_cluster=True/False )


```bash
salt <target> docker_util.swarm_init advertise_addr='ens4' listen_addr='0.0.0.0' force_new_cluster=False
```

**Return Data**

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

##### docker_util.joinswarm(remote_addr, listen_addr, token)

**Note** You have to pass in the token


```bash
salt <target> docker_util.joinswarm 10.1.0.2 0.0.0.0 SWMTKN-1-1yv40emizau5b1hy2x3boj3vcsy7edoldjxooif13kx9jpv97e-ec78dxpr06sfhplqr05nncihn
```

**Return Data**

```yaml
Comment:
   instance-1-minion.c.optimum-tensor-161912.internal has joined the Swarm
Worker/ManagerIP:
   10.1.0.3
```

### The following will leave a Docker Swarm

##### docker_util.leave_swarm(force=True/False)

```bash
root@Salt-Master:~# salt 'instan*' docker_util.leave_swarm force=True
instance-1-minion.c.optimum-tensor-161912.internal:
    |_
      ----------
      Comment:
          instance-1-minion.c.optimum-tensor-161912.internal has left the swarm
```


## Docker Services Salt Module

##### docker_util.service_create(image=str,name=str,command=str,hostname=str,replicas=int,target_port=int,published_port=int)



**Note: You have to have a swarm running for this to work**

Here we are going to create a docker service with salt on the targeted minion. We if your minion is a worker this will not work, the minion will need to have a manager status and not a worker.
Below is targeting a the Salt-Master itself because that is my manager node.


```bash

salt <target> docker_util.service_create image='httpd' name='Test_Service' command=None hostname='apache' replicas=6 target_port=80 published_port=80

```


**Return Data**

```yaml
Salt-Master:
    |_
      ----------
      Command:
          None
      Hostname:
          apache
      Image:
          httpd
      Info:
          Salt-Master has a Docker Swarm Service running named Test_Service
      Minion:
          Salt-Master
      Name:
          Test_Service
      Published_Port:
          80
      Replicas:
          6
      Target_Port:
          80
```

If I run `docker service ls` on the command line you will see the service running with 6 replicas.

```bash
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
pz4nz5j8suo2        Test_Service        replicated          6/6                 httpd               *:80->80/tcp

```
Here is the service spread out accross the master and minion servers.

```bash
root@Salt-Master:~# docker service ps Test_Service
ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
pb4g28xmr4z5        Test_Service.1      httpd               tjones-master       Running             Running 8 minutes ago
mesn2l97veul        Test_Service.2      httpd               instance-1-minion   Running             Running 8 minutes ago
qcp36x0mqumq        Test_Service.3      httpd               tjones-master       Running             Running 8 minutes ago
szc2knyx59d2        Test_Service.4      httpd               instance-1-minion   Running             Running 8 minutes ago
uosngu752xbr        Test_Service.5      httpd               tjones-master       Running             Running 8 minutes ago
0kzzadygz4mh        Test_Service.6      httpd               instance-1-minion   Running             Running 8 minutes ago
```

```bash
root@tjones-master:~# docker ps
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS               NAMES
156411caab98        httpd:latest        "httpd-foreground"   10 minutes ago      Up 10 minutes       80/tcp              Test_Service.3.qcp36x0mqumqiwnbvp7h99cdb
74832f18084e        httpd:latest        "httpd-foreground"   10 minutes ago      Up 10 minutes       80/tcp              Test_Service.5.uosngu752xbr6ps1e4rhnozrr
48831a88a89c        httpd:latest        "httpd-foreground"   10 minutes ago      Up 10 minutes       80/tcp              Test_Service.1.pb4g28xmr4z5m8ag3smg812ib
```
