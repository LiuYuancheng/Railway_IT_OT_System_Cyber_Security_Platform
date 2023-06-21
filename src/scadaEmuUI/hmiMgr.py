#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railwayMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/05/29
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import scadaGobal as gv
from collections import OrderedDict

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSensors(object):
    """ The sensors set to show the sensors detection state."""
    def __init__(self, parent, id, posList=None):
        self.parent = parent
        self.id = id
        self.sensorsCount = 0 if posList is None else len(posList)
        self.sensorsPosList = [] if posList is None else posList
        self.sensorsStateList = [0]*self.sensorsCount 

    def addOneSensor(self, pos):
        self.sensorsPosList.append(pos)
        self.sensorsCount += 1
        self.sensorsStateList.append(0)
    
    def updateSensorState(self, idx, state):
        if idx < self.sensorsCount:
            self.sensorsStateList[idx] = state

    def updateSensorsState(self, statList):
        print("update sensor: %s, in: %s, %s " % (str( self.id), str(self.sensorsCount), str(len(statList)) ))
        if len(statList) == self.sensorsCount:
            self.sensorsStateList = statList

    def getID(self):
        return self.id

    def getSensorsCount(self):
        return self.sensorsCount

    def getSensorPos(self):
        return self.sensorsPosList

    def getSensorsState(self):
        return self.sensorsStateList

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentSignal(object):

    def __init__(self, parent, id, pos) -> None:
        self.parent = parent
        self.id = id
        self.pos = pos
        self.state = False
        self.triggerOnPosList = []
        self.triggerOffPosList = []
    
    def addTGonPos(self, pos):
        self.triggerOnPosList.append(pos)

    def addTFoffPos(self, pos):
        self.triggerOffPosList.append(pos)

    def getID(self):
        return self.id
    
    def getState(self):
        return self.state

    def getPos(self):
        return self.pos
    
    def getTGonPos(self):
        return self.triggerOnPosList
    
    def getTGoffPos(self):
        return self.triggerOffPosList
    
    def setState(self, state):
        self.state = state

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MapMgr(object):
    """ Map manager to init/control differet elements state on the map."""
    def __init__(self, parent):
        """ Init all the elements on the map. All the parameters are public to 
            other module.
        """
        self.sensors = OrderedDict()
        self.signals = OrderedDict()
        self._initSensors()
        self._initSignals()

    def _initSensors(self):
        
        y = 100
        sensorPos_we = [(80+100*i, y) for i in range(17) ]
        self.sensors['weline'] = AgentSensors(self, 'we')
        for pos in sensorPos_we:
            self.sensors['weline'].addOneSensor(pos)

        y += 160
        sensorPos_cc = [(80+120*i, y) for i in range(14)] 
        self.sensors['ccline'] = AgentSensors(self, 'cc')
        for pos in sensorPos_cc:
            self.sensors['ccline'].addOneSensor(pos)

        y+= 160
        sensorPos_ns = [(80+210*i, y) for i in range(8)] 
        self.sensors['nsline'] = AgentSensors(self, 'ns')
        for pos in sensorPos_ns:
            self.sensors['nsline'].addOneSensor(pos)

    def _initSignals(self):
        y = 100
        trackSignalConfig_we = [
            {'id': 'we-0', 'pos':(80+100*1+50, y), 'tiggerS': 'ccline', 'onIdx':(12,), 'offIdx':(13,) },
            {'id': 'we-2', 'pos':(80+100*3+50, y),  'tiggerS': 'ccline', 'onIdx':(10,), 'offIdx':(11,) },
            {'id': 'we-4', 'pos':(80+100*5+50, y),  'tiggerS': 'ccline', 'onIdx':(8,), 'offIdx':(9,) },
            {'id': 'we-6', 'pos':(80+100*7+50, y),  'tiggerS': 'ccline', 'onIdx':(6,), 'offIdx':(7,) },
            {'id': 'we-7', 'pos':(80+100*9+50, y),  'tiggerS': 'ccline', 'onIdx':(6,), 'offIdx':(7,) },
            {'id': 'we-5', 'pos':(80+100*11+50, y),  'tiggerS': 'ccline', 'onIdx':(8,), 'offIdx':(9,) },
             {'id': 'we-3', 'pos':(80+100*13+50, y),  'tiggerS': 'ccline', 'onIdx':(10,), 'offIdx':(11,) },
            {'id': 'we-1', 'pos':(80+100*15+50, y),  'tiggerS': 'ccline', 'onIdx':(12,), 'offIdx':(13,) },            
        ]
        key = 'weline'
        self.signals[key] = []
        
        for signalInfo in trackSignalConfig_we:
            signal = AgentSignal(self, signalInfo['id'], signalInfo['pos'])
            sPosList = self.getSensors(trackID=signalInfo['tiggerS']).getSensorPos()
            for idx in signalInfo['onIdx']:
                signal.addTGonPos(sPosList[idx])
            for idx in signalInfo['offIdx']:
                signal.addTFoffPos(sPosList[idx])
            self.signals[key].append(signal)

        y += 160
        trackSignalConfig_cc = [
            {'id': 'cc-0', 'pos':(80+120*0+60, y), 'tiggerS': 'nsline', 'onIdx':(0, 6), 'offIdx':(1, 7) },
            {'id': 'cc-1', 'pos':(80+120*2+60, y), 'tiggerS': 'nsline', 'onIdx':(4,), 'offIdx':(5,) },
            {'id': 'cc-2', 'pos':(80+120*4+60, y, y), 'tiggerS': 'nsline', 'onIdx':(2,), 'offIdx':(3,) },
            {'id': 'cc-3', 'pos':(80+120*6+60, y),  'tiggerS': 'weline', 'onIdx':(7,9), 'offIdx':(8,10) },
            {'id': 'cc-4', 'pos':(80+120*8+60, y),  'tiggerS': 'weline', 'onIdx':(5,11), 'offIdx':(6,12) },
            {'id': 'cc-5', 'pos':(80+120*10+60, y),  'tiggerS': 'weline', 'onIdx':(3,13), 'offIdx':(4,14) },
            {'id': 'cc-6', 'pos':(80+120*12+60, y),  'tiggerS': 'weline', 'onIdx':(1, 15), 'offIdx':(2,16) },
        ]
        key = 'ccline'
        self.signals[key] = []
        for signalInfo in trackSignalConfig_cc:
            signal = AgentSignal(self, signalInfo['id'], signalInfo['pos'])
            sPosList = self.getSensors(trackID=signalInfo['tiggerS']).getSensorPos()
            for idx in signalInfo['onIdx']:
                signal.addTGonPos(sPosList[idx])
            for idx in signalInfo['offIdx']:
                signal.addTFoffPos(sPosList[idx])
            self.signals[key].append(signal)

        y += 160
        trackSignalConfig_ns = [
            {'id': 'ns-0', 'pos':(80+210*0+100, y), 'tiggerS': 'ccline', 'onIdx':(0,), 'offIdx':(1,) },
            {'id': 'ns-1', 'pos':(80+210*2+100, y), 'tiggerS': 'ccline', 'onIdx':(0,), 'offIdx':(1,) },
            {'id': 'ns-2', 'pos':(80+210*4+100, y), 'tiggerS': 'ccline', 'onIdx':(2,), 'offIdx':(3,) },
            {'id': 'ns-3', 'pos':(80+210*6+100, y), 'tiggerS': 'ccline', 'onIdx':(4,), 'offIdx':(5,) },
        ]
        key = 'nsline'
        self.signals[key] = []
        for signalInfo in trackSignalConfig_ns:
            signal = AgentSignal(self, signalInfo['id'], signalInfo['pos'])
            sPosList = self.getSensors(trackID=signalInfo['tiggerS']).getSensorPos()
            for idx in signalInfo['onIdx']:
                signal.addTGonPos(sPosList[idx])
            for idx in signalInfo['offIdx']:
                signal.addTFoffPos(sPosList[idx])
            self.signals[key].append(signal)


    def getSensors(self, trackID=None):
        if trackID and trackID in self.sensors.keys(): return self.sensors[trackID]
        return self.sensors

    def getSignals(self, trackID=None):
        if trackID and trackID in self.signals.keys(): return self.signals[trackID]
        return self.signals
    
    def setSensors(self, trackID, stateList):
        self.sensors[trackID].updateSensorsState(stateList)

    def setSingals(self, trackID, stateList):
        if len(stateList) <= len(self.signals[trackID]):
            for i, state in enumerate(stateList):
                 self.signals[trackID][i].setState(state)