# illumio.core.cven role  

- [Container Host Requirements](#container-host-requirements)
    - [CVEN Compatibility](#cven-compatibility)
- [Installation](#installation)
    - [Requirements](#requirements)
- [Usage Examples](#usage-examples)
- [Role Variables](#role-variables)
    - [Policy Compute Engine (PCE)](#policy-compute-engine-pce)
    - [Kubelink](#kubelink)
    - [Pairing Profile](#pairing-profile)
    - [CVEN](#cven)
- [License](#license)

## Container Host Requirements  

This role will work with the following container orchestration platforms:

- Azure Kubernetes Service (AKS)
- Kubernetes
- IBM Cloud Kubernetes Service (IKS)
- Rancher Kubernetes Engine (RKE)
- OpenShift

> **Note:** see the [Illumio Support dependencies page](https://support.illumio.com/shared/software/os-support-package-dependencies/cven_kubelink.html) for specific CVEN and Kubelink compatibility details  

### CVEN Compatibility  

PCE Version  | CVEN 19.3.6 | CVEN 21.1 | CVEN 21.2 | CVEN 21.5
------------ | :---------: | :-------: | :-------: | :-------:
21.2         | X           | X         | X         | 
21.5         | X           | X         | X         | X
22.2         | X           | X         | X         | X
22.5         | X           | X         | X         | X

## Installation  

You can install this role with: `ansible-galaxy install illumio.core.cven`  

### Requirements  

This module requires Python 3.8+ and the `illumio` python package installed on the Ansible controller.  

The `cven` role depends on the `kubelink` role in order to function - see the `kubelink` [requirements](KUBELINK_ROLE.md#requirements).  

## Usage Examples  

**Example inventory file**  

```ini
[kube]
10.0.7.13   ansible_connection=ssh  ansible_user=kubernetes
10.0.7.14   ansible_connection=ssh  ansible_user=kubernetes
10.0.7.15   ansible_connection=ssh  ansible_user=kubernetes

[kube:vars]
ansible_python_interpreter=/usr/bin/python3
illumio_cven_image_pull_secret=dockerinternal
illumio_cven_container_registry=docker-internal.mycompany.com
illumio_cven_container_name=ven/illumio-ven
illumio_cven_container_version=21.5.40-8601
```

**Example playbook**  

```yml
---
- name: Install CVEN to Kube cluster
  hosts: kube
  gather_facts: yes
  roles:
    - role: illumio.core.cven
```

## Role Variables  

### Policy Compute Engine (PCE)  

Values for the PCE connection details default to the environment variable values in the table below.  

Variable | Description | Data Type | Environment variable | Default value
-------- | ----------- | --------- | -------------------- | -------------
`illumio_pce_hostname` | PCE hostname | `str` | `ILLUMIO_PCE_HOST` | -
`illumio_pce_port` | PCE HTTPS port | `int` | `ILLUMIO_PCE_PORT` | `443`
`illumio_pce_org_id` | PCE Organization ID | `int` | `ILLUMIO_PCE_ORG_ID` | `1`
`illumio_pce_api_key` | PCE API key | `str` | `ILLUMIO_API_KEY_USERNAME` | -
`illumio_pce_api_secret` | PCE API secret | `str` | `ILLUMIO_API_KEY_SECRET` | -
`illumio_pce_tls_verify` | Enable/disable TLS verification | `bool` | - | `true`
`illumio_pce_tls_ca` | Custom root CA path. If set, overrides `illumio_pce_tls_verify` | `str` | - | -
`illumio_pce_tls_client_certs` | TLS client cert paths. Can point to a single PEM file containing public/private pair or two separate files | `list` | - | -
`illumio_pce_http_proxy` | HTTP proxy server | `str` | `http_proxy` | -
`illumio_pce_https_proxy` | HTTPS proxy server | `str` | `https_proxy` | -

### Kubelink  

See the [Kubelink role docs page](KUBELINK_ROLE.md) for details.  

### Pairing Profile  

The CVEN secret requires a pairing key that is used to pair the cluster hosts with the PCE. A pairing profile is created (or reused if one with the given name already exists) and used to generate the key for the CVEN secret.  

Variable | Description | Data Type | Default value
-------- | ----------- | --------- | -------------
`illumio_cven_profile_name` | CVEN pairing profile name | `str` | `PP-ANSIBLE-CVEN`
`illumio_cven_profile_description` | CVEN pairing profile description | `str` | `"CVEN cluster host profile. Created by Ansible"`
`illumio_cven_enforcement_mode` | default enforcement mode for the paired workload. One of `idle`, `visibility_only`, `selective`, or `full` | `str` | `idle`
`illumio_cven_visibility_level` | determines what traffic will be logged by VENs paired with this profile by default. One of `flow_summary`, `flow_drops`, `flow_off`, `enhanced_data_collection` | `str` | `flow_summary`
`illumio_cven_labels` | list of Label HREFs | `list` | -
`illumio_cven_ven_version` | If your PCE's VEN library has multiple versions available, you can specify the version to use. The profile will use the default version configured in the PCE if no value is specified | `str` | -

### CVEN  

See the Illumio [guide on deploying CVENs](https://docs.illumio.com/core/21.5/Content/Guides/kubernetes-and-openshift/deployment/deploy-c-vens-in-your-cluster.htm) for installation details.  

Variable | Description | Data Type | Default value
-------- | ----------- | --------- | -------------
`illumio_cven_namespace` | Kubernetes/OpenShift namespace for CVEN config | `str` | `illumio-system`  
`illumio_cven_secret_name` | CVEN Secret name | `str` | `illumio-ven-config`  
`illumio_cven_container_registry` | Container registry the CVEN image will be pulled from. Registry secrets must be set up in Kubernetes/OpenShift independent of this role | `str` | -
`illumio_cven_image_pull_secret` | imagePullSecret name for authentication to a remote image registry | `str` | -
`illumio_cven_container_name` | CVEN container name | `str` | `illumio-ven`
`illumio_cven_container_version` | image tag version to pull | `str` | `latest`

> **Note:** if using self-signed or private PKI to sign a host PCE certificate, you will need to update the CVEN DaemonSet to reference the root CA certificate. See [the CVEN deployment documentation](https://docs.illumio.com/core/21.5/Content/Guides/kubernetes-and-openshift/deployment/deploy-c-vens-in-your-cluster.htm#DeployCVENs) for details  

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
