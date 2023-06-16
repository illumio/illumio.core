===========
 Changelog
===========

Version 0.2.6 (TBD)
-------------------

* increment `illumio` python library version requirement to 1.1.3

FEATURES:

* Label module - create/update/delete label objects in the PCE

IMPROVEMENTS:

* add the following options to all PCE modules:
    * `pce_tls_verify` - flag denoting whether TLS verification should be enabled on the PCE connection
    * `pce_tls_ca` - path to a custom root CA certificate bundle to use for the PCE connection
    * `pce_tls_client_certs` - paths to client-side certificate files
    * `pce_http_proxy` - HTTP proxy server to use when connecting to the PCE
    * `pce_https_proxy` - HTTPS proxy server to use when connecting to the PCE

Version 0.2.5 (June 12, 2023)
-----------------------------

* remove support for EOL Ansible versions (2.9, 2.10, 2.11)
* update roles to support v2.14+ linting rules

BUG FIXES:

* check if ven_status.rc is defined in ven_status task failed_when clause

Version 0.2.4 (October 14, 2022)
--------------------------------

IMPROVEMENTS:

* increment `illumio` python library version requirement to 1.1.1
* rename collection from `illumio.illumio` to `illumio.core`
* initial Galaxy release

Version 0.2.3 (July 15, 2022)
-----------------------------

BUG FIXES:

* fix Windows compatibility for VEN role
    * fix powershell script for Windows pairing
    * separate management tasks to use Linux-/Windows-specific modules
    * delegate PCE object module calls to localhost to work with Windows remotes

Version 0.2.2 (July 09, 2022)
-----------------------------

* fix issues found with `ansible-test sanity`

IMPROVEMENTS:

* update role documentation to include expected data types for role variables

Version 0.2.1 (July 09, 2022)
-----------------------------

FEATURES:

* `ven_library` role - add new VEN versions to the PCE VEN library
* `ven` role - add role tags for VEN management
    * `ven_start`
    * `ven_stop`
    * `ven_restart`
    * `ven_suspend`
    * `ven_unsuspend`
    * `ven_deactivate`
    * `ven_unpair`

IMPROVEMENTS:

* updated all roles to meet `ansible-lint` specifications
* improve role documentation

Version 0.2.0 (Jun 29, 2022)
----------------------------

* automate container cluster setup and sync

FEATURES:

* `kubelink` role - pair Kubernetes/OpenShift clusters with the PCE, monitor namespaces
* `cven` role - pair Kubernetes/OpenShift nodes with the PCE
* Pairing profile module - create/update/delete pairing profile objects in the PCE
* Pairing key module - generate pairing keys from existing profiles
* Container cluster module - create/update/delete container cluster objects in the PCE

Version 0.1.1 (Apr 27, 2022)
----------------------------

* initial implementation

FEATURES:

* `ven` role - pair/unpair workloads with the PCE
