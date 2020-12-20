minions = [i.strip() for i in open("test.txt").readlines()]
inventory = [_.strip() for _ in open("patching.txt").readlines()]

for _ in minions:
        minion = _.replace("-",".").replace("nm","10.140").replace("idc","10.120")
        if minion not in inventory:
                print(_+" or ", end =" ")