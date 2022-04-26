# illumio.illumio.ven role  


## Installation  

## Role Variables  

### Policy Compute Engine (PCE)  

`illumio_pce_hostname` - PCE hostname (e.g. my.pce.com)  
`illumio_pce_port` - PCE HTTPS port (defaults to 443)  
`illumio_pce_org_id` - PCE Organization ID (defaults to 1)  
`illumio_pce_api_key` - PCE API key  
`illumio_pce_api_secret` - PCE API secret  

### Pairing profile  

`illumio_pairing_profile_id` - pairing profile ID to use when pairing hosts. By default, a temporary pairing profile will be created to pair each VEN, then torn down once pairing is complete  

### Teardown  

`illumio_ven_unpair` - if set to true, unpairs the VEN from the PCE  
`illumio_ven_firewall_restore` - the strategy to use when restoring the firewall state after the VEN is unpaired. Must be one of "default", "saved", or "disable". The default is "default". This variable has no effect if `illumio_ven_unpair` is not set to true  
