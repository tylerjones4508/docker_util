import docker
import os
import subprocess
import salt.config
import salt.loader
__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
server_name = __grains__['id']
client = docker.from_env()




def service_create(image=str,name=str,command=str):
    d = []
    client.services.create(name=name, image=image, command=command)
    echoback = server_name + ' has a docker service running named ' + name
    d.append({'Info': echoback, 'Name': name, 'Image': image})
    print d


service_create(image='ubuntu',name='python-test',command='tail -f /dev/null')
