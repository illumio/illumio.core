# illumio.illumio.ven role


## Installation

## Role Variables

### Policy Compute Engine (PCE)

`illumio_pce_hostname` : PCE hostname (e.g. my.pce.com)
`illumio_pce_port` : PCE HTTPS port (defaults to 443)
`illumio_pce_org_id` : PCE Organization ID (defaults to 1)
`illumio_pce_api_key` : PCE API key
`illumio_pce_api_secret` : PCE API secret

### Pairing profile

`illumio_pairing_profile_id` : OPTIONAL - pairing profile ID to use when pairing hosts

### Teardown

`illumio_ven_unpair` : OPTIONAL - if set to true, unpairs the VEN from the PCE
