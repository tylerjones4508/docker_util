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
    echoback = server_name + ' has a docker service running named ' + name
    d.append({'Info': echoback, 'Name': name, 'Image': image})
    print d


service_create(image='ubuntu',name='python-test',command='tail -f /dev/null',hostname='testcont',replicas=5,target_port=80,published_port=80)
