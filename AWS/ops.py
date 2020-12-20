#!/usr/bin/env python3.7
import json
from aws.template import Template, Output
from aws.intrinsicfunctions import Ref, GetAtt, Select, Cidr, Base64, Join

t = Template()

def create_vpc(stack_properties: dict(), config : dict()):
    from aws.workers import get_azes
    from aws.resources import VPC, Subnet, InternetGateway, VPCGatewayAttachment, EIP, NatGateway, RouteTable, Route, SubnetRouteTableAssociation, SecurityGroup, SecurityGroupIngress, SecurityGroupEgress

    cidr = config[stack_properties['Environment']][stack_properties['Service']]['cidr']
    subnetcount = config[stack_properties['Environment']][stack_properties['Service']]['subnetcount']
    subnetmask = config[stack_properties['Environment']][stack_properties['Service']]['subnetmask']
    s = az = 0
    fazes =list()
    azes = get_azes(config['region'])

    while s<subnetcount:
        if az is len(azes):
            az = 0
        else:
            fazes.append(azes[az])
            az+=1
            s+=1

    t.set_resource(VPC( ResourceId="vpc", 
                        CidrBlock=cidr, 
                        EnableDnsSupport="true", 
                        EnableDnsHostnames="true", 
                        InstanceTenancy="default", 
                        Tags=[{ "Key": "Name", 
                                "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-vpc"}]))

    for _ in range(subnetcount):
        t.set_resource(Subnet(  ResourceId = F"S{_}", 
                                AvailabilityZone = fazes[_], 
                                CidrBlock = Select(_, Cidr(cidr,subnetcount, subnetmask)), 
                                VpcId = Ref("vpc"), 
                                Tags=[{"Key": "Name", 
                                        "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-S{_}"}]))

    t.set_resource(InternetGateway( ResourceId="igw", 
                                    Tags=[{ "Key": "Name", 
                                            "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-igw"}]))
    t.set_resource(VPCGatewayAttachment(ResourceId="igwattachment", 
                                        DependsOn="igw", 
                                        VpcId=Ref("vpc"), 
                                        InternetGatewayId=Ref("igw")))

    t.set_resource(EIP( ResourceId="neip", 
                        Domain="vpc"))
    
    t.set_resource(NatGateway(  ResourceId="ngw", 
                                DependsOn="igwattachment", 
                                AllocationId=GetAtt("neip", "AllocationId"), 
                                SubnetId=Ref("S1"), 
                                Tags=[{ "Key": "Name", 
                                        "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-ngw"}]))

    t.set_resource(RouteTable(  ResourceId="PublicRt", 
                                VpcId=Ref("vpc"), 
                                Tags=[{ "Key": "Name", 
                                        "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-PublicRt"}]))
    t.set_resource(Route(   ResourceId="PublicRouteAddition", 
                            RouteTableId=Ref("PublicRt"), 
                            DestinationCidrBlock = "0.0.0.0/0", 
                            GatewayId = Ref("igw")))

    t.set_resource(RouteTable(  ResourceId="PrivateRt", 
                                VpcId=Ref("vpc"), 
                                Tags=[{ "Key": "Name", 
                                        "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-PrivateRt"}]))
    t.set_resource(Route(ResourceId="PrivateRtAddition", 
                        RouteTableId=Ref("PrivateRt"), 
                        DestinationCidrBlock = "0.0.0.0/0", 
                        NatGatewayId = Ref("ngw")))

    for _ in range(subnetcount):
        if _%2 is 0:
            t.set_resource(SubnetRouteTableAssociation( ResourceId=F"S{_}RTA", 
                                                        RouteTableId = Ref("PublicRt"), 
                                                        SubnetId = Ref(F"S{_}")))
        else:
            t.set_resource(SubnetRouteTableAssociation( ResourceId=F"S{_}RTA", 
                                                        RouteTableId = Ref("PrivateRt"), 
                                                        SubnetId = Ref(F"S{_}")))

    t.set_resource(SecurityGroup(ResourceId="CustomSg", 
                                 DependsOn = "vpc", 
                                 GroupDescription = "SG for new VPC", 
                                 VpcId=Ref("vpc"), 
                                 Tags=[{"Key": "Name", 
                                 "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-CustomSg"}]))

    t.set_resource(SecurityGroupIngress(ResourceId = "SgRuleSshSelf", 
                                        DependsOn = "CustomSg", 
                                        GroupId = Ref("CustomSg"), 
                                        IpProtocol = "tcp", 
                                        FromPort = "22", 
                                        ToPort = "22", 
                                        SourceSecurityGroupId = Ref("CustomSg")))

    for _ in config[stack_properties['Environment']][stack_properties['Service']]['allowedports']['inbound']:
        t.set_resource(SecurityGroupIngress(ResourceId = "SgRuleSshIBS", 
                                            DependsOn = "CustomSg", 
                                            GroupId = Ref("CustomSg"), 
                                            IpProtocol = "tcp", 
                                            FromPort = _['port'], 
                                            ToPort = _['port'], 
                                            CidrIp = _['source']))

    t.set_resource(SecurityGroupEgress( ResourceId = "SgRuleAllTraffic", 
                                        DependsOn = "CustomSg", 
                                        GroupId = Ref("CustomSg"), 
                                        IpProtocol = "-1", 
                                        FromPort = "0", 
                                        ToPort = "0", 
                                        CidrIp = "0.0.0.0/0"))
    
    t.set_output(Output(Name = "vpc", 
                        Value = Ref("vpc"), 
                        ExportName = F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-vpc"))
    
    for _ in range(subnetcount):
        t.set_output(Output(Name = F"Subnet{_}", 
                            Value = Ref(F"S{_}"), 
                            ExportName = F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-Subnet{_}"))
    
    t.set_output(Output(Name = "sgid", 
                        Value = Ref("CustomSg"), 
                        ExportName = F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-CustomSg"))

    return t

def create_ec2_instance(stack_properties: dict(), config : dict()):
    from aws.resources import Instance
    conf = config[stack_properties['Environment']][stack_properties['Service']]
    for _ in range(1, conf['Count']+1):
        t.set_resource(Instance(ResourceId=F"ec2i{_}", 
                                ImageId=conf['ImageId'], 
                                InstanceInitiatedShutdownBehavior=conf['InstanceInitiatedShutdownBehavior'], 
                                InstanceType=conf['InstanceType'], 
                                KeyName=conf['KeyName'], 
                                NetworkInterfaces=[{"AssociatePublicIpAddress": conf['AssociatePublicIpAddress'],                                 "DeviceIndex": "0", 
                                                    "SubnetId": conf['SubnetId'], 
                                                    "GroupSet": [conf['SecurityGroupId']]}], 
                                BlockDeviceMappings = [{"DeviceName" : "/dev/sda1", 
                                                        "Ebs" : { 
                                                                "VolumeType" : conf['VolumeType'], 
                                                                "DeleteOnTermination" : conf['DeleteVolumeOnTermination'], "VolumeSize" : conf['VolumeSize']}}], 
                                Tags=[{"Key": "Name", "Value": F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-Instance_1"}],
                                UserData=Base64(Join("",[
                                                "#!/bin/bash -xe\n",
                                                "apt update\n",
                                                "apt-get install default-jdk -y\n",
                                                "wget https://pkg.jenkins.io/debian-stable/binary/jenkins_2.176.1_all.deb -P /tmp/\n",
                                                "apt install /tmp/jenkins_2.176.1_all.deb -y"
                                            ]))
                                
        ))
        
        t.set_output(Output(Name = F"PublicIP{_}", 
                            Value = GetAtt(F"ec2i{_}", "PublicIp"), 
                            ExportName = F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-PublicIp-{_}"))
        t.set_output(Output(Name = F"PublicDnsName{_}", 
                            Value = GetAtt(F"ec2i{_}", "PublicDnsName"), 
                            ExportName = F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-PublicDnsName-{_}"))
        t.set_output(Output(Name = F"PrivateIp{_}", 
                            Value = GetAtt(F"ec2i{_}", "PrivateIp"), 
                            ExportName = F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}-PrivateIp-{_}")) 
    return t

