import docker
import os
import subprocess
import salt.config
import salt.loader
__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
client = docker.from_env()
server_name = __grains__['id']


def swarm_init(advertise_addr=str,
               listen_addr=int,
               force_new_cluster=bool):
    '''
    Initalize Docker on Minion as a Swarm Manager
    salt <Target> advertise_addr='ens4' listen_addr='0.0.0.0:5000' force_new_cluster=False
    '''
    d = []
    client.swarm.init(advertise_addr,
                      listen_addr,
                      force_new_cluster)
    output =  'Docker swarm has been Initalized on '+   server_name  + ' and the worker/manager Join token is below'
    command = "docker swarm join-token worker | xargs | awk '{print $16}' "
    manager_command = "docker swarm join-token manager | xargs | awk '{print $16}' "
    token = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE)
    key  = token.communicate()[0]
    manager_token = subprocess.Popen(manager_command,
                                     shell=True,
                                     stdout=subprocess.PIPE)
    key_2 = manager_token.communicate()[0]
    d.append({'Comment': output,
              'Worker_Token': key,
              'Manger_Token': key_2 })
    return d

def joinswarm(remote_addr=int,
              listen_addr=int,
              token=str):
    '''
    Join a Swarm Worker to the cluster
    *NOTE this can be use for worker or manager join
    salt <target> 10.1.0.1 0.0.0.0 token
    '''
    d = []
    client.swarm.join(remote_addrs=[remote_addr],
                      listen_addr=listen_addr,
                      join_token=token )
    output =  server_name + ' has joined the Swarm'
    d.append({'Comment': output,
              'Worker/ManagerIP': remote_addr })
    return d



def leave_swarm(force=bool):
    '''
    Will force the minion to leave the swarm
    '''
    d = []
    client.swarm.leave(force=force)
    output = server_name + ' has left the swarm'
    d.append({'Comment': output})
    return d



def service_create(image=str,
                   name=str,
                   command=str,
                   hostname=str,
                   replicas=int,
                   target_port=int,
                   published_port=int):
    d = []
    replica_mode = docker.types.ServiceMode('replicated', replicas=replicas)
    ports = docker.types.EndpointSpec(ports={ target_port: published_port })
    client.services.create(name=name,
                           image=image,
                           command=command,
                           mode=replica_mode,
                           endpoint_spec=ports)
    echoback = server_name + ' has a Docker Swarm Service running named ' + name
    d.append({'Info': echoback,
              'Minion': server_name,
              'Name': name,
              'Image': image,
              'Command': command,
              'Hostname': hostname,
              'Replicas': replicas,
              'Target_Port': target_port,
              'Published_Port': published_port})
    return d


def list_swarm_services():
    d = []
    command = 'docker service ls'
    runner = subprocess.Popen(command,
                              shell=True,
                              stdout=subprocess.PIPE)
    output  = runner.communicate()[0]
    d.append({'Minion': server_name,'Docker Services': output})
    return d


def ps_docker_service(service_name=str):
    d = []
    command = 'docker service ps ' + service_name
    runner = subprocess.Popen(command,
                              shell=True,
                              stdout=subprocess.PIPE)
    output  = runner.communicate()[0]
    return_name = 'Docker Service PS ' + server_name
    d.append({'Minion': server_name, return_name: output})
    return d
