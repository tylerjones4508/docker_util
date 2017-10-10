import docker
import os
import subprocess
import salt.config
import salt.loader
import json
__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
client = docker.from_env()
server_name = __grains__['id']

def swarm_tokens():
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    service = client.inspect_swarm()
    return service['JoinTokens']


def swarm_init(advertise_addr=str,
               listen_addr=int,
               force_new_cluster=bool):
    '''
    Initalize Docker on Minion as a Swarm Manager
    salt <Target> advertise_addr='ens4' listen_addr='0.0.0.0:5000' force_new_cluster=False
    '''
    d = {}
    client.swarm.init(advertise_addr,
                      listen_addr,
                      force_new_cluster)
    output =  'Docker swarm has been Initalized on '+   server_name  + ' and the worker/manager Join token is below'
    d.update({'Comment': output,
              'Tokens': swarm_tokens()})
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
    return_name = 'Docker Service PS ' + service_name
    d.append({'Minion': server_name, return_name: output})
    return d


def swarm_service_info(service_name=str):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    d = {}
    service = client.inspect_service(service=service_name)
    getdata = json.dumps(service)
    dump = json.loads(getdata)
    name = dump['Spec']['Name']
    network_mode = dump['Spec']['EndpointSpec']['Mode']
    ports = dump['Spec']['EndpointSpec']['Ports']
    swarm_id = dump['ID']
    create_date = dump['CreatedAt']
    update_date = dump['UpdatedAt']
    labels = dump['Spec']['Labels']
    replicas =  dump['Spec']['Mode']['Replicated']['Replicas']
    network = dump['Endpoint']['VirtualIPs']
    image = dump['Spec']['TaskTemplate']['ContainerSpec']['Image']
    for items in ports:
        published_port = items['PublishedPort']
        target_port = items['TargetPort']
        published_mode = items['PublishMode']
        protocol = items['Protocol']
        d.update({'Service Name': name,
                  'Replicas': replicas,
                  'Service ID': swarm_id,
                  'Network': network,
                  'Network Mode': network_mode,
                  'Creation Date': create_date,
                  'Update Date': update_date,
                  'Published Port': published_port,
                  'Target Port': target_port,
                  'Published Mode': published_mode,
                  'Protocol': protocol,
                  'Docker Image': image,
                  'Minion Id': server_name})
                   
    return d

def remove_service(service=str):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    d = {}
    service = client.remove_service(service)
    d.update({'Service Deleted':service,
              'Minion ID': server_name })
    return d    


def node_ls():
    d = {}
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    service = client.nodes(filters=None)
    getdata = json.dumps(service)
    dump = json.loads(getdata)
    for items in dump:
        docker_version = items['Description']['Engine']['EngineVersion']
        platform = items['Description']['Platform']
        hostnames = items['Description']['Hostname']
        ids = items['ID']
        role = items['Spec']['Role']
        availability = items['Spec']['Availability'] 
        status =  items['Status']
        d.update({'Docker Version': docker_version,
                  'Platform': platform,
                  'Hostname': hostnames,
                  'ID': ids,
                  'Roles': role,
                  'Availability': availability,
                  'Status': status})
        return d
    

    
