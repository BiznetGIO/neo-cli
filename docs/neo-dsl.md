# NEO DSL

## Structure

```yaml
<category>:
  <name_entity>:
  parameters:
    <parameter_1_key> : <paramater_1_value>
    <parameter_2_key> : <paramater_2_value>
  template: <template>
```

## Templates

### Cluster

#### Kubernetes

parameters :

key | value | requirement | description
---|---|---|---
image | string | no | -
controller_flavor | string | no | -
master_flavor | string | yes | -
worker_flavor | string | yes | -
public_network | string | no | -
master_size | number | yes | -
worker_size | number | yes | -
private_network | string | yes | -

example :

```yaml
clusters:
  neo-k8s:
    template: "kubernetes"
    parameters:
      master_flavor: SS2.1
      worker_flavor: SS2.1
      master_size: 1
      worker_size: 1
    deploy:
    - clusters.neo-k8s
```

### Networks

#### Private (Private network)

parameters :

key | value | requirement | description
---|---|---|---
gateway | string (example :192.168.0.1) | yes | -
cidr | string (example :192.168.0.0/24) | yes | -
dns | string (example :8.8.8.8) | no | -

### Instances

#### vm (Virtual Machine)

parameters :

key | value | requirement | description
---|---|---|---
private_network | string | yes | -
key_name | string | yes | -
image | string | yes | -
flavor | string | yes | -
username | string | yes | -

example :

```yaml
deploy:
- others.key-coba
- networks.neowork-coba
- instances.vm-coba
instances:
  vm-coba:
    parameters:
      flavor: SS2.1
      image: CentOS 7.3
      key_name: key-coba
      private_network: neowork-coba
      username: ibnu
    template: vm
networks:
  neowork-coba:
    parameters:
      cidr: 192.168.3.0/24
      gateway: 192.168.3.1
    template: private
others:
  key-coba:
    template: key-pairs
```

#### plesk (Plesk Bundle)

parameters :

key | value | requirement | description
---|---|---|---
private_network | string | yes | -
key_name | string | yes | -
image | string | yes | -
flavor | string | yes | -
username | string | yes | -
email | string | yes | -
password | string | yes | -
activation_key | string | yes | -
floating_desc | string | no | set description to floating ip
neo_type  | {"metadata": {"neo_type": <metadata_type>}} | no | add metadata to neo vm


### Others

#### key_pairs

parameters : no parameters
