# illumio.core.ven role  

- [Host Requirements](#host-requirements)
    - [Operating System](#operating-system)
    - [VEN Compatibility](#ven-compatibility)
- [Installation](#installation)
    - [Requirements](#requirements)
- [Usage Examples](#usage-examples)
- [Role Variables](#role-variables)
    - [Policy Compute Engine (PCE)](#policy-compute-engine-pce)
    - [Pairing Profile](#pairing-profile)
    - [Unpair](#unpair)
- [Tags](#tags)
    - [ven_pair](#venpair)
    - [ven_start](#venstart)
    - [ven_stop](#venstop)
    - [ven_restart](#venrestart)
    - [ven_suspend](#vensuspend)
    - [ven_unsuspend](#venunsuspend)
    - [ven_deactivate](#vendeactivate)
    - [ven_unpair](#venunpair)
- [License](#license)

## Host Requirements  

### Operating System  

This role will work with the following operating systems (see the compatibility chart below for a more detailed breakdown):

- AIX
- Amazon Linux
- Amazon Linux 2
- Debian
- Red Hat Enterprise Linux
- SUSE Enterprise Linux
- Solaris
- Ubuntu
- Windows

### VEN Compatibility  

PCE Version  | VEN 21.2.x | VEN 21.5.x | VEN 22.2.x | VEN 22.5.22
------------ | :--------: | :--------: | :--------: | :---------:
21.2         | X          |            |            | 
21.5         | X          | X          |            | 
22.2         | X          | X          | X          | 
22.5         | X          | X          | X          | X

See the [Illumio Support dependencies page](https://support.illumio.com/software/os-support-package-dependencies/ven.html) for specific VEN OS compatibility details.  

## Installation  

You can install this role with: `ansible-galaxy install illumio.core.ven`

### Requirements  

This module requires Python 3.8+ and the `illumio` python package installed on the Ansible controller.  

In Ansible 2.10 and higher, modules have been moved into collections. Additional collections beyond `ansible.builtin` must now be installed explicitly. For this role, make sure the following collections are installed:  

```sh
ansible-galaxy collection install ansible.windows
ansible-galaxy collection install community.general
```

> **Note:** these dependencies are included when installing the `illumio.core` collection with `ansible-galaxy collection install illumio.core`  

## Usage Examples  

**Example inventory file**  

```ini
[apache_servers]
10.0.9.212   ansible_connection=ssh  ansible_user=jdoe

[apache_servers:vars]
ansible_python_interpreter=/usr/bin/python3
```

**Example playbook**  

```yml
---
- name: Install Illumio VENs on Apache Web Server workloads
  hosts: apache_servers
  gather_facts: yes
  roles:
    - role: illumio.core.ven
```

**Example commands**  

```sh
# pair
$ ansible-playbook -i apache_hosts ven_install.yml

# check status
$ ansible-playbook -i apache_hosts ven_install.yml --tags ven_status

# unpair
$ ansible-playbook -i apache_hosts ven_install.yml --tags ven_unpair
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

### Pairing profile  

VEN pairing requires a key that is used to pair the remote workloads with the PCE. A pairing profile is created (or reused if one with the given name already exists) and used to generate the key used for pairing. If a profile with the given name exists, **its configuration will be overwritten with values provided to the role**.  

Variable | Description | Data Type | Default value
-------- | ----------- | --------- | -------------
`illumio_ven_profile_name` | pairing profile to use when pairing hosts. If the profile does not exist it will be created. | `str` | `PP-ANSIBLE-VEN`
`illumio_ven_profile_description` | pairing profile description | `str` | `"Ansible VEN role pairing profile"`
`illumio_ven_enforcement_mode` | default enforcement mode for the paired workload. One of `idle`, `visibility_only`, `selective`, or `full` | `str` | `idle`
`illumio_ven_visibility_level` | determines what traffic will be logged by VENs paired with this profile by default. One of `flow_summary`, `flow_drops`, `flow_off`, `enhanced_data_collection` | `str` | `flow_summary`
`illumio_ven_labels` | list of Label HREFs | `list` | -
`illumio_ven_version` | If your PCE's VEN library has multiple versions available, you can specify the version to use. The profile will use the default version configured in the PCE if no value is specified | `str` | -

### Unpair  

Used when running the role with the [`ven_unpair`](#ven_unpair) tag.  

`illumio_ven_firewall_restore` - the strategy to use when restoring the firewall state after the VEN is unpaired. Must be one of `recommended`, `saved`, `open`, or `unmanaged` (Windows only). Defaults to `recommended`. This variable has no effect if `illumio_ven_unpair` is not set to true  

    recommended    Remove all firewall rules and apply recommended policy (allow SSH/22 and ICMP only).
    saved          Remove all applied Illumio rules and policy from the current firewall.
    open           Remove all firewall rules and leave all ports open.
    unmanaged      Windows only. Reverts to the workload's currently configured Windows Firewall policy.

## Tags  

VEN management operations can be run by specifying one of the tags below when running the `illumio.core.ven` role.  

See the chapter on [VEN State](https://docs.illumio.com/core/21.5/Content/Guides/ven-administration/ven-state/_ch-ven-state.htm) in the VEN adminisrtation guide for more detailed explanations of each state.  

### ven_pair  

The default behaviour for the `illumio.core.ven` role. Creates a pairing profile (or uses an existing one if `illumio_ven_profile_name` is passed) and generates a pairing key to pair remote workloads with the PCE.  

### ven_start  

Starts VEN processes and sync with the PCE. If the VEN was stopped, the PCE will change the workload from offline to online.  

### ven_stop  

Stops all VEN processes and sends a "goodbye" message to the PCE. The PCE marks the workload as offline and triggers a policy recomputation. Security policy rules configured by the VEN are not removed from the workload firewall.  

### ven_restart  

Stop and start the VEN. VEN processes will be shut off and restarted, and policy will be recomputed for the workload.  

### ven_suspend  

Put the VEN into a suspended state: firewall rules configured on the workload by the PCE are removed and all VEN software is shut down.  

The workload remains visible in the PCE, but updates to suspended state. This mode can be useful for troubleshooting connectivity issues to or between workloads where the VEN could be the cause of the disruption.  

### ven_unsuspend  

Removes the VEN from a suspended state: the VEN software is started and firewall rules are reapplied according to security policy rules in the PCE.  

### ven_deactivate  

Breaks the connection between the VEN and the PCE, but leaves the VEN software installed on the workload.  

After the VEN is deactivated, the workload firewall is restored to its previous settings.  

> **Note:** this action is **irreversible** through the VEN role. To reactivate the VEN, you will need run `illumio_ven_ctl activate` manually or unpair and repair the workload  

### ven_unpair  

Removes the VEN and corresponding workload record from the PCE and uninstalls the VEN software from the workload.  

The workload firewall is restored to a state based on the `illumio_ven_firewall_restore` value passed to the unpair command.  

To understand the specific actions taken by the VEN during unpairing, see [VEN Unpairing Details](https://docs.illumio.com/core/21.5/Content/Guides/ven-administration/rollback-deactivate-or-uninstall-vens/ven-unpairing-details.htm) in the VEN administration guide.  

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
