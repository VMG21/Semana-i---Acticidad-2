import pyrebase
import psutil
import time
import json
import re


def getListOfProcessSortedByMemory():
    listOfProcObjects = []

    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects

def parse_frec(message):
    x = re.search("\(([^\)]+)\)", message)
    a = x.group()
    a = a.replace("(", "")
    a = a.replace(")", "")
    a = a.replace(" ", "")
    a = a.split(",")
    a = a[0].replace("current=", "")
    return float(a)

def parse_nuc(message): return int(message[0])

def parse_uso(message): return int(message[0])

def parse_mem(message):
    x = message.split(",")
    x = x[2]
    x = x.replace(" ", "")
    x = x.replace("percent=", "")
    return float(x)

def parse_proc(message):
    x = re.search("name[^,]+", message)
    a = x.group()
    a = a.replace("name': '", "")
    a = a.replace("'", "")
    return a


while True:
    i = 0
    for i in range(7):
        print(i)
        data = json.load(open('config1.json'))

        configs = data[i]
        # print(configs)

        firebase = pyrebase.initialize_app(configs)
        db = firebase.database()

        listOfRunningProcess = getListOfProcessSortedByMemory()

        frec = parse_frec(str(psutil.cpu_freq()))
        nuc = parse_nuc(str(psutil.cpu_count()))
        uso = parse_uso(str(psutil.cpu_percent(4)))
        mem = parse_mem(str(psutil.virtual_memory()))
        proc = parse_proc(str(listOfRunningProcess[0]))

        data = {
            "frec": frec,
            "nuc": nuc,
            "uso": uso,
            "mem": mem,
            "proc": proc
        }

        db.child("users").child("victor").update(data)
    
    time.sleep(120)
    