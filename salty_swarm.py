import docker
import os
import subprocess
import salt.config
import salt.loader
__opts__ = salt.config.minion_config('/etc/salt/minion')
__grains__ = salt.loader.grains(__opts__)
client = docker.from_env()
server_name = __grains__['id']

'''
Initalize Docker on Minion as a Swarm Manager
* Does not work on Windows OS at the moment
`salt <Target> advertise_addr='ens4' listen_addr='0.0.0.0:5000' force_new_cluster=False`
'''


def swarm_init(advertise_addr=str,listen_addr=int, force_new_cluster=bool ):
    d = []
    client.swarm.init(advertise_addr, listen_addr,force_new_cluster)
    output =  'Docker swarm has been Initalized on '+   server_name  + ' and the worker/manager Join token is below'
    command = "docker swarm join-token worker | xargs | awk '{print $16}' "
    manager_command = "docker swarm join-token manager | xargs | awk '{print $16}' "
    token = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    key  = token.communicate()[0]
    manager_token = subprocess.Popen(manager_command, shell=True, stdout=subprocess.PIPE)
    key_2 = manager_token.communicate()[0]
    d.append({'Comment': output, 'Worker_Token': key, 'Manger_Token': key_2 })
    return d

'''
Join a Swarm Worker to the cluster
*NOTE this can be use for worker or manager join
 `salt <target> 10.1.0.1 0.0.0.0 token ``
'''


def joinswarm(remote_addr, listen_addr, token):
    d = []
    client.swarm.join(remote_addrs=[remote_addr], listen_addr=listen_addr, join_token=token )
    output =  server_name + ' has joined the Swarm'
    d.append({'Comment': output, 'Worker/ManagerIP': remote_addr })
    return d

'''
Will force the minion to leave the swarm
'''

def leave_swarm(force=bool):
    d = []
    client.swarm.leave(force=force)
    output = server_name + ' has left the swarm'
    d.append({'Comment': output})
    return d
