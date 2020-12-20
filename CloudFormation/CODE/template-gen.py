#!/usr/bin/env python3
'''
    The troposphere module in used to genegrate cloudformation templates. In this case we are dependent on this module. We can create the same template with full control using Data classes. This is only for Demonstration. All the AWS related tasks will be done using Data class and objects
'''

import cfops
from boto3 import client
from troposphere import Template, Ref, Tags, Output, Select, Cidr, GetAtt, Export, Join
from troposphere.ec2 import VPC, Subnet, InternetGateway, VPCGatewayAttachment, EIP, NatGateway, RouteTable, Route, SubnetRouteTableAssociation, SecurityGroup, SecurityGroupIngress, SecurityGroupEgress

@profile
def main():
    stackname = "ystack"
    cidr = "10.10.0.0/16"
    subnetcount = 12
    subnetmask = 9
    s = az = 0
    fazes =[]
    typ = ""

    azes = client('ec2').describe_availability_zones()['AvailabilityZones']
    while s<subnetcount:
        if az is len(azes):
            az = 0
        else:
            fazes.append(azes[az]['ZoneName'])
            az+=1
            s+=1

    t = Template()
    t.add_version("2010-09-09")
    t.add_resource([
        VPC(
            "vpc",
            EnableDnsSupport = "true",
            CidrBlock = cidr,
            EnableDnsHostnames = "true",
            InstanceTenancy = "default",
            Tags = Tags(
                Name = F"{stackname}-VPC-{cidr.split('/')[0]}"
            )
        ),
        InternetGateway('igw'),
        VPCGatewayAttachment(
            'igwattachment',
            DependsOn="igw",
            VpcId=Ref("vpc"),
            InternetGatewayId=Ref("igw")
        ),
        EIP(
            'neip',
            Domain = "vpc"
        ),
        NatGateway(
            'ngw',
            DependsOn = "igwattachment",
            AllocationId = GetAtt("neip", "AllocationId"),
            SubnetId = Ref("S0")
        ),
        RouteTable(
            'PublicRt',
            VpcId = Ref("vpc")
        ),
        RouteTable(
            'PrivateRt',
            VpcId = Ref("vpc")
        ),
        Route(
            'PublicRouteAddition',
            RouteTableId = Ref("PublicRt"),
            DestinationCidrBlock = "0.0.0.0/0",
            GatewayId = Ref("igw")
        ),
        Route(
            'PrivateRtAddition',
            RouteTableId = Ref("PrivateRt"),
            DestinationCidrBlock = "0.0.0.0/0",
            NatGatewayId = Ref("ngw")
        ),
        SecurityGroup(
            'CustomSg',
            DependsOn = "vpc",
            GroupDescription = "SG for us-east-1-10.10.0.0-VPC",
            VpcId = Ref("vpc"),
            Tags = Tags(
                Name = F"{stackname}-Default-SG"
            )
        ),
        SecurityGroupIngress(
            'SgRuleSshSelf',
            DependsOn = "CustomSg",
            GroupId = Ref("CustomSg"),
            IpProtocol = "tcp",
            FromPort = "22",
            ToPort = "22",
            SourceSecurityGroupId = Ref("CustomSg")
        ),
        SecurityGroupIngress(
            'SgRuleSshIBS',
            DependsOn = "CustomSg",
            GroupId = Ref("CustomSg"),
            IpProtocol = "tcp",
            FromPort = "22",
            ToPort = "22",
            CidrIp = "203.122.24.146/32"
        ),
        SecurityGroupEgress(
            'SgRuleAllTraffic',
            DependsOn = "CustomSg",
            GroupId = Ref("CustomSg"),
            IpProtocol = "-1",
            FromPort = "0",
            ToPort = "0",
            CidrIp = "0.0.0.0/0"
        )
    ])

    for _ in range(subnetcount):
        if _%2 is 0:
            typ = "Public"
        else:
            typ = "Private"
        t.add_resource(Subnet(
            F"S{_}",
            AvailabilityZone = fazes[_],
            CidrBlock = Select(_, Cidr(cidr,subnetcount, subnetmask)),
            VpcId = Ref("vpc"),
            Tags = Tags(
                Name = F"{stackname}-{typ}-Subnet"
            )
        ))

    for _ in range(subnetcount):
        if _%2 is 0:
            t.add_resource(SubnetRouteTableAssociation(
                F"S{_}RTA",
                RouteTableId = Ref("PublicRt"),
                SubnetId = Ref(F"S{_}")
            ))
        else:
            t.add_resource(SubnetRouteTableAssociation(
                F"S{_}RTA",
                RouteTableId = Ref("PrivateRt"),
                SubnetId = Ref(F"S{_}")
            ))

    t.add_output([
        Output(
            'vpc',
            Value = Ref("vpc"),
            Export = Export(F"{stackname}-VPCID")
        ),
        Output(
            'sgid',
            Value = Ref("CustomSg"),
            Export = Export(F"{stackname}-SecurityGroupID")
        ),
        Output(
            'PublicSubnets',
            Value = Join(", ", [Ref("S0"), Ref("S2"), Ref("S4"), Ref("S6"), Ref("S8"), Ref("S10")]),
            Export = Export(F"{stackname}-PublicSubnetsList")
        ),
        Output(
            'PrivateSubnests',
            Value = Join(", ", [Ref("S1"), Ref("S3"), Ref("S5"), Ref("S7"), Ref("S9"), Ref("S11")]),
            Export = Export(F"{stackname}-PrivateSubnetsList")
        )
    ])

#cfops.create_cf_stack(stackname,t.to_yaml())
if __name__ == "__main__":
    main()