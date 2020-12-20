#!/usr/bin/env python3.7

from .template import _Resource

class VPC(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "CidrBlock" : String,
        "EnableDnsSupport" : Boolean,
        "EnableDnsHostnames" : Boolean,
        "InstanceTenancy" : String,
        "Tags" : [ Resource Tag, ... ]
        """
        super().__init__("AWS::EC2::VPC", **kwargs)

class Subnet(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "AssignIpv6AddressOnCreation" : Boolean,
        "AvailabilityZone" : String,
        "CidrBlock" : String,
        "Ipv6CidrBlock" : String,
        "MapPublicIpOnLaunch" : Boolean,
        "Tags" : [ Resource Tag, ... ],
        "VpcId" : String
        """
        super().__init__("AWS::EC2::Subnet", **kwargs)

class InternetGateway(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id"
        """
        super().__init__("AWS::EC2::InternetGateway", **kwargs)

class VPCGatewayAttachment(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "InternetGatewayId" : String,
        "VpcId" : String,
        "VpnGatewayId" : String
        """
        super().__init__("AWS::EC2::VPCGatewayAttachment", **kwargs)

class EIP(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "Domain" : String,
        "InstanceId" : String,
        "PublicIpv4Pool" : String
        """
        super().__init__("AWS::EC2::EIP", **kwargs)

class NatGateway(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "AllocationId" : String,
        "SubnetId" : String,
        "Tags" : [ Resource Tag, ... ]
        """
        super().__init__("AWS::EC2::NatGateway", **kwargs)

class RouteTable(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "VpcId" : String
        """
        super().__init__("AWS::EC2::RouteTable", **kwargs)

class Route(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "DestinationCidrBlock" : String,
        "DestinationIpv6CidrBlock" : String,
        "EgressOnlyInternetGatewayId" : String,
        "GatewayId" : String,
        "InstanceId" : String,
        "NatGatewayId" : String,
        "NetworkInterfaceId" : String,
        "RouteTableId" : String,
        "VpcPeeringConnectionId" : String
        """
        super().__init__("AWS::EC2::Route", **kwargs)

class SubnetRouteTableAssociation(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "RouteTableId" : String,
        "SubnetId" : String
        """
        super().__init__("AWS::EC2::SubnetRouteTableAssociation", **kwargs)

class SecurityGroup(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "GroupName" : String,
        "GroupDescription" : String,
        "SecurityGroupEgress" : [ Security Group Rule, ... ],
        "SecurityGroupIngress" : [ Security Group Rule, ... ],
        "Tags" :  [ Resource Tag, ... ],
        "VpcId" : String
        """
        super().__init__("AWS::EC2::SecurityGroup", **kwargs)

class SecurityGroupIngress(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "CidrIp" : String,
        "CidrIpv6" : String,
        "Description" : String,
        "FromPort" : Integer,
        "GroupId" : String,
        "GroupName" : String,
        "IpProtocol" : String,
        "SourcePrefixListId" : String,
        "SourceSecurityGroupName" : String,
        "SourceSecurityGroupId" : String,
        "SourceSecurityGroupOwnerId" : String,
        "ToPort" : Integer
        """
        super().__init__("AWS::EC2::SecurityGroupIngress", **kwargs)

class SecurityGroupEgress(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "CidrIp" : String,
        "CidrIpv6" : String,
        "Description" : String,
        "DestinationPrefixListId" : String,
        "DestinationSecurityGroupId" : String,
        "FromPort" : Integer,
        "GroupId" : String,
        "IpProtocol" : String,
        "ToPort" : Integer
        """
        super().__init__("AWS::EC2::SecurityGroupEgress", **kwargs)

class Instance(_Resource):
    def __init__(self, **kwargs):
        """
        "ResourceId": "id",
        "AdditionalInfo" : String,
        "Affinity" : String,
        "AvailabilityZone" : String,
        "BlockDeviceMappings" : [ BlockDeviceMapping, ... ],
        "CreditSpecification" : CreditSpecification,
        "DisableApiTermination" : Boolean,
        "EbsOptimized" : Boolean,
        "ElasticGpuSpecifications" : [ ElasticGpuSpecification, ... ],
        "ElasticInferenceAccelerators" : [ ElasticInferenceAccelerator, ... ],
        "HostId" : String,
        "IamInstanceProfile" : String,
        "ImageId" : String,
        "InstanceInitiatedShutdownBehavior" : String,
        "InstanceType" : String,
        "Ipv6AddressCount" : Integer,
        "Ipv6Addresses" : [ InstanceIpv6Address, ... ],
        "KernelId" : String,
        "KeyName" : String,
        "LaunchTemplate" : LaunchTemplateSpecification,
        "LicenseSpecifications" : [ LicenseSpecification, ... ],
        "Monitoring" : Boolean,
        "NetworkInterfaces" : [ NetworkInterface, ... ],
        "PlacementGroupName" : String,
        "PrivateIpAddress" : String,
        "RamdiskId" : String,
        "SecurityGroupIds" : [ String, ... ],
        "SecurityGroups" : [ String, ... ],
        "SourceDestCheck" : Boolean,
        "SsmAssociations" : [ SsmAssociation, ... ],
        "SubnetId" : String,
        "Tags" : [ Tag, ... ],
        "Tenancy" : String,
        "UserData" : String,
        "Volumes" : [ Volume, ... ]
        """
        super().__init__("AWS::EC2::Instance", **kwargs)

class IAMRole(_Resource):
    def __init__(self, **kwargs):
        """
        "AssumeRolePolicyDocument" : Json,
        "ManagedPolicyArns" : [ String, ... ],
        "MaxSessionDuration" : Integer,
        "Path" : String,
        "PermissionsBoundary" : String,
        "Policies" : [ Policy, ... ],
        "RoleName" : String
        """
        super().__init__("AWS::IAM::Role", **kwargs)

class IAMPolicy(_Resource):
    def __init__(self, **kwargs):
        """
        "Groups" : [ String, ... ],
        "PolicyDocument" : Json,
        "PolicyName" : String,
        "Roles" : [ String, ... ],
        "Users" : [ String, ... ]
        """
        super().__init__("AWS::IAM::Policy", **kwargs)

class IAMInstanceProfile(_Resource):
    def __init__(self, **kwargs):
        """
        "InstanceProfileName" : String,
        "Path" : String,
        "Roles" : [ String, ... ]
        """
        super().__init__("AWS::IAM::InstanceProfile", **kwargs)

class EKS_Cluster(_Resource):
    def __init__(self, **kwargs):
        """
        "Name" : String,
        "ResourcesVpcConfig" : ResourcesVpcConfig,
        "RoleArn" : String,
        "Version" : String
        """
        super().__init__("AWS::EKS::Cluster", **kwargs)

class AutoScalingGroup(_Resource):
    def __init__(self, **kwargs):
        """
        """
        super().__init__("AWS::AutoScaling::AutoScalingGroup", **kwargs)

class LaunchConfiguration(_Resource):
    def __init__(self, **kwargs):
        """
        """
        super().__init__("AWS::AutoScaling::LaunchConfiguration", **kwargs)