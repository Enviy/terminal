import socket
import subprocess


def getIPs():
    list = []
    values = subprocess.run('arp -a', shell=True, capture_output=True)
    for i in values.stdout.decode("utf-8").split('('):
        if len(i) > 5:
            list.append(i.split(')')[0])
    return list


def pscan(t, p):
    try:
        con = socket.socket.connect((t, p))
        return True
    except:
        return False


def scannit():
    output = {}
    ips = getIPs()
    if ips:
        for i in ips:
            print('[*] Running scan for {0}'.format(i))
            for p in range(0, 1024):
                if pscan(i, p):
                    print('ip: {0} - port: {1} is open'.format(i, p))
                    output[i].append(p)
    return output
