Changelog
=========

Version 0.2.2 (July 09, 2022)
-----------

* fix issues found with `ansible-test sanity`

IMPROVEMENTS:

* update role documentation to include expected data types for role variables

Version 0.2.1 (July 09, 2022)
-----------

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
-----------

* automate container cluster setup and sync

FEATURES:

* `kubelink` role - pair Kubernetes/OpenShift clusters with the PCE, monitor namespaces
* `cven` role - pair Kubernetes/OpenShift nodes with the PCE
* Pairing profile module - create/update/delete pairing profile objects in the PCE
* Pairing key module - generate pairing keys from existing profiles
* Container cluster module - create/update/delete container cluster objects in the PCE

Version 0.1.1 (Apr 27, 2022)
-----------

* initial implementation

FEATURES:

* `ven` role - pair/unpair workloads with the PCE
