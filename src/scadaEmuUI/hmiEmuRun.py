#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiEmuRun.py
#
# Purpose:     This module is the main wx-frame for the Human Machine Interface
#              of metro railway and signal SCADA sysetm.
#
# Author:      Yuancheng Liu
#
# Version:     v0.1
# Created:     2023/06/13
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import os
import sys
import time
import wx
import scadaGobal as gv

import hmiPanel as pnlFunction
import hmiMgr as mapMgr
import hmiPanelMap as pnlMap
import scadaDataMgr as dataMgr

PERIODIC = 500      # update in every 500ms
FRAME_SIZE = (1800, 1030)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""

    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetTransparent(gv.gTranspPct*255//100)
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        self._initGlobals()
        self._buildMenuBar()
        # Build UI sizer
        self.digitalInLBList= None
        self.digitalOutLBList = None
        self._initDigitalLbs()

        self.SetSizer(self._buidUISizer())

        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' %str(gv.TEST_MD))

        self.updateLock = False
        if not gv.TEST_MD:
            gv.idataMgr = dataMgr.DataManager(self, gv.gPlcInfo)
        # Set the periodic call back
        self.updatePlcConIndicator()
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(PERIODIC)  # every 500 ms


#-----------------------------------------------------------------------------
    def _initGlobals(self):
        # Init the global parameters used only by this module
        gv.gTrackConfig['weline'] = {'id': 'weline',
                                    # weline junction sensors connected to holding register idx on PLC-00/01/02
                                    'sensorIdx': (0, 17), 'signalIdx': (0, 8), 
                                    # weline station sensors connected to holding register idx on PLC-03/04/05
                                    'stationSensorIdx': (0, 10), 'stationSignalIdx': (0, 10),
                                    'color': wx.Colour(52, 169, 129), 'icon': 'welabel.png'}
        
        gv.gTrackConfig['nsline'] = {'id': 'nsline',
                                    # nsline junction sensors connected to holding register idx on PLC-00/01/02
                                    'sensorIdx': (17, 25), 'signalIdx': (8, 12),
                                    # nsline station sensors connected to holding register idx on PLC-03/04/05
                                    'stationSensorIdx': (10, 16), 'stationSignalIdx': (10, 16),
                                    'color': wx.Colour(233, 0, 97), 'icon': 'nslabel.png'}
        
        gv.gTrackConfig['ccline'] = {'id': 'ccline', 
                                    # ccline junction sensors connected to holding register idx on PLC-00/01/02
                                    'sensorIdx': (25, 39), 'signalIdx': (12, 19),
                                    # ccline station sensors connected to holding register idx on PLC-03/04/05
                                    'stationSensorIdx': (16, 22), 'stationSignalIdx': (16, 22),
                                    'color': wx.Colour(255, 136, 0), 'icon': 'cclabel.png'}
        # Init all the global instance
        gv.iMapMgr = mapMgr.MapMgr(self)

#--UIFrame---------------------------------------------------------------------
    def _initDigitalLbs(self):
        self.digitalInLBList= {}
        self.digitalOutLBList ={}
        welineColor = gv.gTrackConfig['weline']['color']
        nslineColor = gv.gTrackConfig['nsline']['color']
        cclineColor = gv.gTrackConfig['ccline']['color']
        # init the PLC-00
        self.digitalInLBList['PLC-00'] = []
        for i in range(0, 15):
            data = {'item': 'wes'+str(i).zfill(2), 'color':welineColor}
            self.digitalInLBList['PLC-00'].append(data)
        
        self.digitalOutLBList['PLC-00'] = []
        for i in range(0, 7):
            data = {'item': 'Swe'+str(i).zfill(2), 'color':welineColor}
            self.digitalOutLBList['PLC-00'].append(data)
       
        # init the PLC-01
        self.digitalInLBList['PLC-01'] = []
        for i in range(0, 2):
            data = {'item': 'wes'+str(i+14).zfill(2), 'color':welineColor}
            self.digitalInLBList['PLC-01'].append(data)
        for i in range(0, 8):
            data = {'item': 'nss'+str(i).zfill(2), 'color':nslineColor}
            self.digitalInLBList['PLC-01'].append(data)
        for i in range(0, 5):
            data = {'item': 'ccs'+str(i).zfill(2), 'color':cclineColor}
            self.digitalInLBList['PLC-01'].append(data)
        
        self.digitalOutLBList['PLC-01'] = []
             
        data = {'item': 'Swe'+str(7).zfill(2), 'color':welineColor}
        self.digitalOutLBList['PLC-01'].append(data)
        for i in range(0, 4):
            data = {'item': 'Sns'+str(i).zfill(2), 'color':nslineColor}
            self.digitalOutLBList['PLC-01'].append(data)
        for i in range(0, 2):
            data = {'item': 'Scc'+str(i).zfill(2), 'color':cclineColor}
            self.digitalOutLBList['PLC-01'].append(data)
    
        # init the PLC-02
        self.digitalInLBList['PLC-02'] = []
        for i in range(4, 13):
            data = {'item': 'Scc'+str(i).zfill(2), 'color':cclineColor}
            self.digitalInLBList['PLC-02'].append(data)

        self.digitalOutLBList['PLC-02'] = []
        for i in range(2, 7):
            data = {'item': 'Scc'+str(i).zfill(2), 'color':cclineColor}
            self.digitalOutLBList['PLC-02'].append(data)

      # init the PLC-03
        self.digitalInLBList['PLC-03'] = []
        for i in range(0, 8):
            data = {'item': 'west'+str(i).zfill(2), 'color':welineColor}
            self.digitalInLBList['PLC-03'].append(data)

        self.digitalOutLBList['PLC-03'] = []
        for i in range(0, 8):
            data = {'item': 'STwe'+str(i).zfill(2), 'color':welineColor}
            self.digitalOutLBList['PLC-03'].append(data)


      # init the PLC-04
        self.digitalInLBList['PLC-04'] = []
        for i in range(8, 10):
            data = {'item': 'west'+str(i).zfill(2), 'color':welineColor}
            self.digitalInLBList['PLC-04'].append(data)
        for i in range(0, 6):
            data = {'item': 'nsst'+str(i).zfill(2), 'color':nslineColor}
            self.digitalInLBList['PLC-04'].append(data)

        self.digitalOutLBList['PLC-04'] = []
        for i in range(8, 10):
            data = {'item': 'STwe'+str(i).zfill(2), 'color':welineColor}
            self.digitalOutLBList['PLC-04'].append(data)
        for i in range(0, 6):
            data = {'item': 'STns'+str(i).zfill(2), 'color':nslineColor}
            self.digitalOutLBList['PLC-04'].append(data)

    # Init the PLC-05
        self.digitalInLBList['PLC-05'] = []
        for i in range(0, 6):
            data = {'item': 'ccst'+str(i).zfill(2), 'color':cclineColor}
            self.digitalInLBList['PLC-05'].append(data)

        self.digitalOutLBList['PLC-05'] = []
        for i in range(0, 6):
            data = {'item': 'STcc'+str(i).zfill(2), 'color':cclineColor}
            self.digitalOutLBList['PLC-05'].append(data)

#--UIFrame---------------------------------------------------------------------
    def _buildMenuBar(self):
        menubar = wx.MenuBar()  # Creat the function menu bar.
        # Add the config menu
        
        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 200,text = "Help",kind = wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')

        self.SetMenuBar(menubar)


#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.VERTICAL)
        mSizer.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label="Railway SCADA HMI")
        label.SetFont(font)
        mSizer.Add(label, flag=flagsL, border=2)
        mSizer.AddSpacer(10)
        gv.iMapPanel = self.mapPanel = pnlMap.PanelMap(self)
        mSizer.Add(gv.iMapPanel, flag=wx.CENTER, border=2)
        mSizer.AddSpacer(10)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(1790, -1),
                                style=wx.LI_HORIZONTAL), flag=flagsL, border=5)

        mSizer.AddSpacer(5)
        # label2 = wx.StaticText(self, label="PLC Monitor Panels [Signal system]")
        # label2.SetFont(font)
        # mSizer.Add(label2, flag=flagsL, border=2)
        # mSizer.AddSpacer(5)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.plcPnls = {}

        signalSz = self._buildPlcPnlsSizer("PLC Monitor Panels [Signal system]", ('PLC-00', 'PLC-01', 'PLC-02'))
        hbox1.Add(signalSz, flag=flagsL, border=2)
        hbox1.AddSpacer(10)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 400),
                                style=wx.LI_VERTICAL), flag=flagsL, border=5)

        stationSZ = self._buildPlcPnlsSizer("PLC Monitor Panels [Station]", ('PLC-03', 'PLC-04', 'PLC-05'))
        hbox1.Add(stationSZ, flag=flagsL, border=2)
        hbox1.AddSpacer(10)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 400),
                        style=wx.LI_VERTICAL), flag=flagsL, border=5)
        hbox1.AddSpacer(10)
        #label2 = wx.StaticText(self, label="Maintenance-Track Place Holder")
        #label2.SetFont(font)
        #hbox1.Add(label2, flag=flagsL, border=2)

        # for key, val in gv.gPlcPnlInfo.items():
        #     hbox1.AddSpacer(10)
        #     ipaddr = val['ipaddress'] + ' : ' + str(val['port'])
        #     self.plcPnls[key] = pnlFunction.PanelPLC(self, val['label'], ipaddr)
        #     hbox1.Add(self.plcPnls[key], flag=flagsL, border=2)
        
        mSizer.Add(hbox1, flag=flagsL, border=2)
        return mSizer

#--UIFrame---------------------------------------------------------------------
    def _buildPlcPnlsSizer(self, PanelTitle, panelKeySeq):
        flagsL = wx.LEFT
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label=PanelTitle)
        label.SetFont(font)
        vSizer.Add(label, flag=flagsL, border=2)
        vSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        for key in panelKeySeq:
            hbox1.AddSpacer(10)
            panelInfo = gv.gPlcPnlInfo[key]
            ipaddr = panelInfo['ipaddress'] + ' : ' + str(panelInfo['port'])


            dInInfoList =  self.digitalInLBList[key] if key in self.digitalInLBList.keys() else None
            dOutInfoList = self.digitalOutLBList[key] if key in self.digitalOutLBList.keys() else None
            self.plcPnls[key] = pnlFunction.PanelPLC(self, panelInfo['label'], ipaddr, 
                                                     dInInfoList=dInInfoList,
                                                     dOutInfoList=dOutInfoList)
            hbox1.Add(self.plcPnls[key], flag=flagsL, border=2)
        
        vSizer.Add(hbox1, flag=flagsL, border=2)
        return vSizer
        
#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            if not gv.TEST_MD:
                if gv.idataMgr: gv.idataMgr.periodic(now)
                # update the PLC display panel
                for key in self.plcPnls.keys():
                    # update the holding registers
                    tgtPlcID = gv.gPlcPnlInfo[key]['tgt']
                    rsIdx, reIdx = gv.gPlcPnlInfo[key]['hRegsInfo']
                    registList = gv.idataMgr.getPlcHRegsData(tgtPlcID, rsIdx, reIdx)
                    print(registList)
                    self.plcPnls[key].updateHoldingRegs(registList)
                    csIdx, ceIdx = gv.gPlcPnlInfo[key]['coilsInfo']
                    coilsList = gv.idataMgr.getPlcCoilsData(tgtPlcID, csIdx, ceIdx)
                    print(coilsList)
                    self.plcPnls[key].updateCoils(coilsList)
                    self.plcPnls[key].updateDisplay()
                
                # update all the junction sensor and signals
                for key in gv.gTrackConfig.keys():
                    signalTgtPlcID = 'PLC-00'
                    rsIdx, reIdx = gv.gTrackConfig[key]['sensorIdx']
                    registList = gv.idataMgr.getPlcHRegsData(signalTgtPlcID, rsIdx, reIdx)
                    print(key)
                    gv.iMapMgr.setSensors(key, registList)
                    csIdx, ceIdx = gv.gTrackConfig[key]['signalIdx']
                    coilsList = gv.idataMgr.getPlcCoilsData(signalTgtPlcID, csIdx, ceIdx)
                    gv.iMapMgr.setSingals(key, coilsList)

                # update all the station sensros and signals
                for key in gv.gTrackConfig.keys():
                    tgtPlcID = 'PLC-03'
                    rsIdx, reIdx = gv.gTrackConfig[key]['stationSensorIdx']
                    registList = gv.idataMgr.getPlcHRegsData(tgtPlcID, rsIdx, reIdx)
                    print(key)
                    gv.iMapMgr.setStationsSensors(key, registList)
                    csIdx, ceIdx = gv.gTrackConfig[key]['stationSignalIdx']
                    coilsList = gv.idataMgr.getPlcCoilsData(tgtPlcID, csIdx, ceIdx)
                    gv.iMapMgr.setStationsSignals(key, coilsList)

            self.mapPanel.periodic(now)

#-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(' If there is any bug, please contact: \n\n \
                        Author:      Yuancheng Liu \n \
                        Email:       liu_yuan_cheng@hotmail.com \n \
                        Created:     2023/05/02 \n \
                        GitHub Link: https://github.com/LiuYuancheng/Metro_emulator \n', 
                    'Help', wx.OK)

#-----------------------------------------------------------------------------
    def updatePlcConIndicator(self):
        if gv.idataMgr:
            for key in self.plcPnls.keys():
                plcID = gv.gPlcPnlInfo[key]['tgt']
                self.plcPnls[key].setConnection(gv.idataMgr.getConntionState(plcID))


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.APP_NAME[0])
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
