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

### The following will create a Docker Swarm Manager (docker_util.swarm_init)

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


### Display Join Tokens on swarm manager (docker_util.swarm_tokens)

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

### The following will join a minion or master to a Docker Swarm (docker_util.joinswarm)

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

### Leave Swarm (docker_util.leave_swarm)

##### docker_util.leave_swarm(force=bool)

**Leave a Swarm**

```bash
salt 'minion2' docker_util.leave_swarm force=False
```

**Return Data**

```yaml
minion2:
    ----------
    Comment:
        minion2 has left the swarm
```

### Create a Docker Swarm Service (docker_util.service_create)

##### docker_util.service_create(image=str,name=str,command=str,hostname=str,replicas=int,target_port=int,published_port=int) 

***Create Docker Swarm service Note: Needs to be targeted on a Manager***


```bash
salt 'saltmaster' docker_util.service_create image=httpd name=Test_Service command=None hostname=salthttpd replicas=6 target_port=80 published_port=80
```
**Return Data**

```yaml
saltmaster:
    ----------
    Command:
        None
    Hostname:
        salthttpd
    Image:
        httpd
    Info:
        saltmaster has a Docker Swarm Service running named Test_Service
    Minion:
        saltmaster
    Name:
        Test_Service
    Published_Port:
        80
    Replicas:
        6
    Target_Port:
        80

```

**Output of docker service ls**

```bash
root@saltmaster:~# docker service ls
ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
3sgiwf8wzcsc        Test_Service        replicated          6/6                 httpd               *:80->80/tcp
```


### Swarm Service Information (docker_util.swarm_service_info)

##### docker_util.swarm_service_info(service_name=str)

***Shows information about a Swarm Service. Note: Needs to target a Docker Swarm Manager***

```bash
salt saltmaster docker_util.swarm_service_info service_name=Test_Service
```

**Return Data**

```yaml
saltmaster:
    ----------
    Creation Date:
        2017-10-11T22:58:56.904144684Z
    Docker Image:
        httpd
    Minion Id:
        saltmaster
    Network:
        |_
          ----------
          Addr:
              10.255.0.6/16
          NetworkID:
              lb1hy71qt33jz2cgxghurjbeu
    Network Mode:
        vip
    Protocol:
        tcp
    Published Mode:
        ingress
    Published Port:
        80
    Replicas:
        6
    Service ID:
        3sgiwf8wzcscu3kp9jhc8np88
    Service Name:
        Test_Service
    Target Port:
        80
    Update Date:
        2017-10-11T22:58:56.908098582Z
    Version:
        29

```

### Remove Docker Service (docker_util.remove_service)

##### docker_util.remove_service(service=str)

***Removes a Service from a Swarm, Note: Needs to target a Manger node***

```bash
salt 'saltmaster' docker_util.remove_service service=Test_Service
```
**Return Data**

```yaml
saltmaster:
    ----------
    Minion ID:
        saltmaster
    Service Deleted:
        True

```

### Show information about a docker swarm node (docker_util.node_ls)

#### docker_util.node_ls(server=str)

***Displays information on a docker node. Similar to `docker node ls` NOTE: needs to target a manager node***

```bash
salt 'saltmaster' docker_util.node_ls server=minion1
```

**Return Data**

```yaml
saltmaster:
    ----------
    Availability:
        active
    Docker Version:
        17.09.0-ce
    Hostname:
        minion1
    ID:
        shze0yxodkpq2cw1i8jze6r1a
    Platform:
        ----------
        Architecture:
            x86_64
        OS:
            linux
    Roles:
        manager
    Status:
        ----------
        Addr:
            192.168.50.11
        State:
            ready
    Version:
        16

```

```bash
salt 'saltmaster' docker_util.node_ls server=saltmaster
```

**Return Data**

```yaml
saltmaster:
    ----------
    Availability:
        active
    Docker Version:
        17.09.0-ce
    Hostname:
        saltmaster
    ID:
        n4hd2xdt5z2abhox5cp611cno
    Platform:
        ----------
        Architecture:
            x86_64
        OS:
            linux
    Roles:
        manager
    Status:
        ----------
        Addr:
            192.168.50.10
        State:
            ready
    Version:
        9

```
