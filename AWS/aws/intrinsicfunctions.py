#!/usr/bin/env python3.7
def Ref(logicalName:str) -> dict:
    return dict(Ref=logicalName)

def Select(index:str, listOfObjects:list) -> dict:
    return dict({'Fn::Select' : [index, listOfObjects]})

def Cidr(ipBlock, subnetcount, subnetmask) -> dict:
    return dict({'Fn::Cidr' : [ipBlock, subnetcount, subnetmask]})

def GetAtt(logicalNameOfResource, attributeName) -> dict:
    return dict({'Fn::GetAtt' : [ logicalNameOfResource, attributeName ]})

def Join(delimiter, listOfObjects:list) -> dict:
    return dict({'Fn::Join' : [delimiter, listOfObjects]})

def Base64(valueToEncode:str) -> dict:
    return dict({'Fn::Base64' : valueToEncode})