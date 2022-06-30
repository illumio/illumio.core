# illumio.illumio.kubelink role  

- [Host Requirements](#host-requirements)
    - [Kubelink Compatibility](#kubelink-compatibility)
- [Installation](#installation)
    - [Requirements](#requirements)
- [Role Variables](#role-variables)
    - [Policy Compute Engine (PCE)](#policy-compute-engine-pce)
    - [Kubelink](#kubelink)
    - [Container Cluster](#container-cluster)
- [Tags](#tags)
- [License](#license)

## Container Host Requirements  

This role will work with the following container orchestration platforms:

- Kubernetes
- Azure Kubernetes Service (AKS)
- IBM Cloud Kubernetes Service (IKS)
- Rancher Kubernetes Engine (RKE)
- OpenShift

> **Note:** see the [Illumio Support dependencies page](https://support.illumio.com/shared/software/os-support-package-dependencies/cven_kubelink.html) for specific CVEN and Kubelink compatibility details  

### Kubelink Compatibility  

Kubelink is compatible with **Kubernetes version 1.18+** and **OpenShift version 4.5+**  

PCE Version  | 21.2 | 21.5 
------------ | :--: | :--: 
Kubelink 2.1 |      | X
Kubelink 2.0 | X    | X

## Installation  

You can install this role with: `ansible-galaxy install illumio.illumio.kubelink`  

### Requirements  

You must have an existing container repository containing the Kubelink Docker image. See the [Kubelink documentation](https://docs.illumio.com/core/21.5/Content/Guides/kubernetes-and-openshift/deployment/deploy-kubelink-in-your-cluster.htm?Highlight=kubelink) for details.  

The `kubernetes.core.k8s` collection requires the `kubernetes` python modules to be installed **on both the Ansible host and the Kubernetes/OpenShift nodes**:  

```sh
pip install kubernetes
```

In Ansible 2.10 and higher, modules have been moved into collections. Additional collections beyond `ansible.builtin` must now be installed explicitly. For this role, make sure the following collections are installed:  

```sh
ansible-galaxy collection install kubernetes.core.k8s
```

> **Note:** these dependencies are included when installing the `illumio` collection with `ansible-galaxy collection install illumio.illumio`  

## Role Variables  

### Policy Compute Engine (PCE)  

Variable | Description | Default value
-------- | ----------- | -------------
`illumio_pce_hostname` | PCE hostname | -
`illumio_pce_port` | PCE HTTPS port | `443`
`illumio_pce_org_id` | PCE Organization ID | `1`
`illumio_pce_api_key` | PCE API key | -
`illumio_pce_api_secret` | PCE API secret | -

### Kubelink

> **NOTE:** in addition to the configuration below, the [`kubernetes.core`](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/index.html) modules used by this role use environment variable configuration for any custom authentication or connection details needed for your cluster. See the [`kubernetes.core.k8s` documentation](https://docs.ansible.com/ansible/latest/collections/kubernetes/core/k8s_module.html#ansible-collections-kubernetes-core-k8s-module) for details on configuring authentication, proxies, or client certificates for your cluster.  

If a Kubelink secret exists in the cluster, Container Cluster creation will be skipped and the existing values will be used for the connection. See the Illumio [guide on deploying Kubelink](https://docs.illumio.com/core/21.5/Content/Guides/kubernetes-and-openshift/deployment/deploy-kubelink-in-your-cluster.htm) for details on the secret file.  

Variable | Description | Default value
-------- | ----------- | -------------
`illumio_kubelink_namespace` | Kubernetes/OpenShift namespace for Kubelink config | `illumio-system`  
`illumio_kubelink_secret_name` | Kubelink Secret name | `illumio-kubelink-config`  
`illumio_kubelink_ignore_cert` | Set to true if using a self-signed certificate for an on-prem PCE | `false`  
`illumio_kubelink_log_level` | Kubelink log level; `0` for debug, `1` for info, `2` for warn, or `3` for error | `1`
`illumio_kubelink_container_registry` | Container registry the Kubelink image will be pulled from. Registry secrets must be set up in Kubernetes/OpenShift independent of this role | -
`illumio_kubelink_image_pull_secret` | imagePullSecret name for authentication to a remote image registry | -
`illumio_kubelink_container_name` | Kubelink container name | `illumio-kubelink`
`illumio_kubelink_container_version` | image tag version to pull | `latest`

> **Note:** if using self-signed or private PKI to sign a host PCE certificate, you will need to update the Kubelink deployment to reference the root CA certificate. See [the Kubelink deployment documentation](https://docs.illumio.com/core/21.5/Content/Guides/kubernetes-and-openshift/deployment/deploy-kubelink-in-your-cluster.htm#DeployKubelink) for details  

### Container Cluster  

By default, a new container cluster with a randomized suffix will be created (e.g. `CC-ANSIBLE-nwfhijpv`). If you would like to use an existing container cluster, you can specify a token along with either the cluster name or cluster ID.  

Variable | Description | Default value
-------- | ----------- | -------------
`illumio_container_cluster_token` | Container cluster token to store in the Kubelink secret. Must be set if using `illumio_container_cluster_name` | -
`illumio_container_cluster_name` | Existing container cluster name | -

## License  

Copyright 2022 Illumio  

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
