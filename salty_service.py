import docker
import os
import subprocess
import salt.config
import salt.loader
__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
server_name = __grains__['id']
client = docker.from_env()




def service_create(image=str,name=str,command=str,hostname=str,replicas=int,target_port=int,published_port=int):
    d = []
    replica_mode = docker.types.ServiceMode('replicated', replicas=replicas)
    ports = docker.types.EndpointSpec(ports={ target_port: published_port })
    client.services.create(name=name, image=image, command=command,mode=replica_mode,endpoint_spec=ports)
    echoback = server_name + ' has a Docker Swarm Service running named ' + name
    d.append({'Info': echoback, 'Minion': server_name, 'Name': name, 'Image': image, 'Command': command, 'Hostname': hostname, 'Replicas': replicas, 'Target_Port': target_port, 'Published_Port': published_port})
    return d


