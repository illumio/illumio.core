# illumio.illumio.ven role  

**Table of Contents**
- [Host Requirements](#host-requirements)
    - [Operating System](#operating-system)
    - [VEN Compatibility](#ven-compatibility)
- [Installation](#installation)
    - [Requirements](#requirements)
- [Role Variables](#role-variables)
    - [Policy Compute Engine (PCE)](#policy-compute-engine-pce)
    - [Pairing Profile](#pairing-profile)
    - [Teardown](#teardown)
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

PCE Version | 21.2 | 21.5
----------- | :--: | :--:
VEN 21.2.5  | X    | X
VEN 21.5.20 |      | X

See the [Illumio Support dependencies page](https://support.illumio.com/software/os-support-package-dependencies/ven.html) for specific VEN OS compatibility details.  

## Installation  

You can install this role with: `ansible-galaxy install illumio.illumio.ven`

### Requirements

In Ansible 2.10 and higher, modules have been moved into collections. Additional collections beyond `ansible.builtin` must now be installed explicitly. For this role, make sure the following collections are installed:  

```sh
ansible-galaxy collection install ansible.windows
ansible-galaxy collection install community.general
```

> **Note:** these dependencies are included when installing the `illumio` collection with `ansible-galaxy collection install illumio.illumio`  

## Role Variables  

### Policy Compute Engine (PCE)  

`illumio_pce_hostname` - PCE hostname (e.g. my.pce.com)  
`illumio_pce_port` - PCE HTTPS port (defaults to 443)  
`illumio_pce_org_id` - PCE Organization ID (defaults to 1)  
`illumio_pce_api_key` - PCE API key  
`illumio_pce_api_secret` - PCE API secret  

### Pairing profile  

`illumio_pairing_profile_id` - pairing profile ID to use when pairing hosts. By default, a temporary pairing profile will be created to pair each VEN, then torn down once pairing is complete  

If a profile ID is not specified, the following variables can be set to customize the temporary pairing profile:  

`illumio_ven_enforcement_mode` - default enforcement mode for the paired workload. One of `idle`, `illuminated` or `enforced`. Defaults to `idle`  
`illumio_ven_visibility_level` - Defaults to `flow_summary`  
`illumio_ven_log_traffic` - Defaults to true  

> **Note:** for temporary profiles, the lock options are ignored as they only affect values that can be changed in the pairing script. All values can be changed in the PCE once the workload has been paired.  

`illumio_ven_version` - If your PCE's VEN library has multiple versions available, you can specify the version to use. The profile will use the default version configured in the PCE if no value is specified  

### Teardown  

`illumio_ven_unpair` - if set to true, unpairs the VEN from the PCE  
`illumio_ven_firewall_restore` - the strategy to use when restoring the firewall state after the VEN is unpaired. Must be one of `recommended`, `saved`, or `open`. Defaults to `recommended`. This variable has no effect if `illumio_ven_unpair` is not set to true  


    recommended    Remove all firewall rules and apply recommended policy (allow SSH/22 and ICMP only).
    saved          Remove all applied Illumio rules and policy from the current firewall.
    open           Remove all firewall rules and leave all ports open.


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
