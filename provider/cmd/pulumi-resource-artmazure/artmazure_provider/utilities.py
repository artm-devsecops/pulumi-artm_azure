
import pulumi_azure_native as azure_native

environments : dict() = {
 "dev": ["development" ],
 "test": [ 'testing' ],	
 "uat": [ 'useracceptancetest' ],	
 "it": [ 'integrationtesting' ],	
 "stag": [ 'staging' ],	
 "prep": [ 'preproduction', 'pre-production', 'pre-prod' ],	
 "prod": [ 'production' ]
}

locations : dict() = {
    "cae1": [ "canadaeast" ],
    "cac1": [ "canadacentral" ],
    "use1": [ "eastus" ],
    "use2": [ "eastus2" ],
    "usc1": [ "centralus" ],
    "usw1": [ "westus" ],
    "usw2": [ "westus2" ],
    "usw3": [ "westus3" ]
}

resource_abbrs= {
    "rg": azure_native.resources.ResourceGroup,
    "vnet": azure_native.network.VirtualNetwork,
    "snet": azure_native.network.Subnet,
    "k8s": azure_native.containerservice.ManagedCluster
}

def get_location(location: str) -> str:
    
    for name, value in locations.items():
        if location.lower() == name:
            return name
        
        for sub_location in value:
            if location.lower().replace(' ', '') == sub_location:
                return name
    
    raise Exception(f'Location {location} not found')

def get_environment(environment: str) -> str:
    
    for name, value in environments.items():
        if environment.lower() == name:
            return name
        
        for sub_environment in value:
            if environment.lower().replace(' ', '') == sub_environment:
                return name
    
    raise Exception(f'Environment {environment} not found')
    

def get_resource_name(type: type, location: str, environment: str, name: str, suffix: str = '') -> str:
    resource_abbr = get_resource_abbr(type)
    location = get_location(location)
    environment = get_environment(environment)
    name = get_clean_name(name)
        
    return f'{resource_abbr}{location}{environment}{name}{suffix}'

def get_clean_name(resource_name: str) -> str:
    return resource_name.lower().replace(' ', '').replace('-', '').replace('_', '')

def get_resource_abbr(type: type) -> str:
    for name, value in resource_abbrs.items():
        if type == value:
            return name


