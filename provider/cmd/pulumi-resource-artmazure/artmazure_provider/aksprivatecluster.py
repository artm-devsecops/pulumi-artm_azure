# Copyright 2016-2021, Pulumi Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import Optional

from pulumi import Inputs, ResourceOptions

import pulumi_azure_native as azure_native
import pulumi

import artmazure_provider
from artmazure_provider.utilities import get_resource_name, get_environment


class AksPrivateClusterArgs:

    resource_name: pulumi.Input[str]
    location: pulumi.Input[str]
    environment: pulumi.Input[str]
    suffix: pulumi.Input[str]
    address_prefix: pulumi.Input[str]

    @staticmethod
    def from_inputs(inputs: Inputs) -> 'AksPrivateClusterArgs':
        return AksPrivateClusterArgs(resource_name=inputs['resourceName'], 
                                     location=inputs['location'],
                                     environment=inputs['environment'],
                                     suffix=inputs['suffix'],
                                     tags=inputs['tags'],
                                     address_prefix=inputs['address_prefix'])

    def __init__(self, 
                 resource_name: pulumi.Input[str], 
                 location: pulumi.Input[str],
                 environment: pulumi.Input[str],
                 suffix: pulumi.Input[str],
                 tags: Optional[pulumi.Input[dict]] = None,
                 address_prefix: pulumi.Input[str] = '10.0.0.0/16') -> None:
        self.resource_name  = resource_name
        self.location       = location
        self.environment    = get_environment(environment)
        self.suffix         = suffix
        self.address_prefix = address_prefix


class AksPrivateCluster(pulumi.ComponentResource):
    location: pulumi.Output[str]
    resource_group: pulumi.Output[azure_native.resources.ResourceGroup]
    virtual_network: pulumi.Output[azure_native.network.VirtualNetwork]
    virtual_network_subnet: pulumi.Output[azure_native.network.Subnet]

    def __init__(self,
                 name: str,
                 args: AksPrivateClusterArgs,
                 props: Optional[dict] = None,
                 opts: Optional[ResourceOptions] = None) -> None:

        super().__init__('artmazure:index:AksPrivateCluster', name, props, opts)
        
        resource_group = azure_native.resources.ResourceGroup("rg",  
            resource_group_name     =   get_resource_name(azure_native.resources.ResourceGroup, args.location, args.environment, args.resource_name, args.suffix),
            location                =   args.location, 
            opts                    =   ResourceOptions(parent=self))


        virtual_network = azure_native.network.VirtualNetwork("vnet",
            virtual_network_name    =   get_resource_name(azure_native.network.VirtualNetwork, args.location, args.environment, args.resource_name, args.suffix),
            location                =   resource_group.location,
            resource_group_name     =   resource_group.name,
            address_space           =   azure_native.network.AddressSpaceArgs(
                address_prefixes    =   [args.address_prefix],
            ),
            opts                    =   ResourceOptions(parent=resource_group)
        )
        
        virtual_network_subnet = azure_native.network.Subnet("subnet",
            subnet_name                             =   get_resource_name(azure_native.network.Subnet, args.location, args.environment, args.resource_name, args.suffix),
            address_prefix                          =   args.address_prefix,
            virtual_network_name                    =   virtual_network.name,
            resource_group_name                     =   resource_group.name,
            private_link_service_network_policies   =   azure_native.network.VirtualNetworkPrivateLinkServiceNetworkPolicies.ENABLED,
            private_endpoint_network_policies       =   azure_native.network.VirtualNetworkPrivateEndpointNetworkPolicies.ENABLED,
            opts                                    =   ResourceOptions(parent=virtual_network)
        )
        
        
        
        # k8s = azure_native.containerservice.ManagedCluster("k8s",
        #     name                        =   get_resource_name(azure_native.containerservice.ManagedCluster, args.location, args.environment, args.resource_name, args.suffix),
        #     resource_group_name         =   resource_group.name,
        #     dns_prefix                  =   get_clean_name(args.resource_name),
        #     api_server_access_profile   =   azure_native.containerservice.ManagedClusterAPIServerAccessProfileArgs(
        #         enable_private_cluster  =   True,
        #     )
        # )
        
        self.location                   = args.location
        self.virtual_network            = virtual_network
        self.virtual_network_subnet     = virtual_network_subnet
        self.resource_group             = resource_group
        
        self.register_outputs({
            'location': args.location,
            'resource_group': resource_group,
            'virtual_network': virtual_network,
            'virtual_network_subnet': virtual_network_subnet
        })
        
