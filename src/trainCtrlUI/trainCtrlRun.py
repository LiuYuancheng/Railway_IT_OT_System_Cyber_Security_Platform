#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        TrainCtrlRun.py
#
# Purpose:     This module is the main wx-frame for the metro trains controller
#              sysetm HMI.
#
# Author:      Yuancheng Liu
#
# Version:     v0.1.2
# Created:     2023/07/12
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import os
import time

import wx

import trainCtrlGlobal as gv
import trainCtrlPanel as pnlFunction
import trainDataMgr as dataMgr

FRAME_SIZE = (1880, 1000)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters, No boader frame."""
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        self.SetBackgroundColour(wx.Colour(39, 40, 62))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        #self.SetTransparent(gv.gTranspPct*255//100)
        self._initGlobals()
        # Build UI sizer
        self._buildMenuBar()
        self._initDigitalLbs()
        self.SetSizer(self._buidUISizer())
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' %str(gv.TEST_MD))
        # Init the local parameters:
        self.updateLock = False
        # Turn on all the trains power during init.
        self.turnOnallTrainsPwr()
        # update the plc connection indicator
        self.updatePlcConIndicator()
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.updateLock = False
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(gv.PERIODIC)  # every 500 ms

#--UIFrame---------------------------------------------------------------------
    def _initGlobals(self):
        # Init the global parameters used only by this module
        gv.gTrackConfig['weline'] = {'id':'weline', 'num': 4,
                                     'trainHregIdx': (0, 4), 
                                     'trainCoilIdx': (0, 4),
                                     'color': wx.Colour(52, 169, 129), 'icon': 'welabel.png'}
        
        gv.gTrackConfig['nsline'] = {'id':'nsline', 'num': 3,
                                     'trainHregIdx': (4,7), 
                                     'trainCoilIdx': (4,7),
                                     'color': wx.Colour(233, 0, 97), 'icon': 'nslabel.png'}
        
        gv.gTrackConfig['ccline'] = {'id':'ccline', 'num': 3,
                                     'trainHregIdx': (7,10),
                                     'trainCoilIdx': (7,10),
                                     'color': wx.Colour(255, 136, 0), 'icon': 'cclabel.png'}
        # Init all the display manager and the data manager.
        gv.iMapMgr = dataMgr.MapManager(self)
        if not gv.TEST_MD: gv.idataMgr = dataMgr.DataManager(self, gv.gPlcInfo)


    def _initDigitalLbs(self):
        self.digitalInLBList= {}
        self.digitalOutLBList ={}
        welineColor = gv.gTrackConfig['weline']['color']
        nslineColor = gv.gTrackConfig['nsline']['color']
        cclineColor = gv.gTrackConfig['ccline']['color']

        self.digitalInLBList['PLC-06'] = []
        for i in range(0, 4):
            data = {'item': 'weS'+str(i).zfill(2), 'color':welineColor}
            self.digitalInLBList['PLC-06'].append(data)

        for i in range(0, 3):
            data = {'item': 'nsS'+str(i).zfill(2), 'color':nslineColor}
            self.digitalInLBList['PLC-06'].append(data)

        for i in range(0, 1):
            data = {'item': 'ccS'+str(i).zfill(2), 'color':cclineColor}
            self.digitalInLBList['PLC-06'].append(data)

        self.digitalOutLBList['PLC-06'] = []
        for i in range(0, 4):
            data = {'item': 'weP'+str(i).zfill(2), 'color':welineColor}
            self.digitalOutLBList['PLC-06'].append(data)

        for i in range(0, 3):
            data = {'item': 'nsP'+str(i).zfill(2), 'color':nslineColor}
            self.digitalOutLBList['PLC-06'].append(data)

        for i in range(0, 1):
            data = {'item': 'ccP'+str(i).zfill(2), 'color':cclineColor}
            self.digitalOutLBList['PLC-06'].append(data)

        self.digitalInLBList['PLC-07'] = []
        for i in range(2, 4):
            data = {'item': 'ccS'+str(i).zfill(2), 'color':cclineColor}
            self.digitalInLBList['PLC-07'].append(data)

        self.digitalOutLBList['PLC-07'] = []
        for i in range(2, 4):
            data = {'item': 'ccP'+str(i).zfill(2), 'color':cclineColor}
            self.digitalOutLBList['PLC-07'].append(data)

#--UIFrame---------------------------------------------------------------------
    def _buildMenuBar(self):
        menubar = wx.MenuBar()  # Creat the function menu bar.
        # Add the config menu

        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 120, text="Help", kind=wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')
        self.SetMenuBar(menubar)

#--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        mSizer.AddSpacer(10)
        
        trainPanelSizer = self._buildTrainStateSizer()
        mSizer.Add(trainPanelSizer, flag=flagsL, border=2)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 890),
                    style=wx.LI_VERTICAL), flag=flagsL, border=2)


        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.AddSpacer(5)

        font = wx.Font(16, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        #vSizer.Add(timelabel, flag=flagsL, border=2)
        timeStr = 'Date and time : ' + time.strftime(' %Y - %m - %d %H : %M : %S ',time.localtime(time.time()))
        self.timeInfo = wx.StaticText(self, label=timeStr)
        self.timeInfo.SetFont(font)
        #self.timeInfo.SetBackgroundColour(wx.Colour("WHITE"))
        self.timeInfo.SetForegroundColour(wx.Colour("WHITE"))
        vbox0.Add(self.timeInfo, flag=flagsL, border=2)
        vbox0.AddSpacer(10)

        gv.iInfoPanel = pnlFunction.PanelTrainInfo(self)
        vbox0.Add(gv.iInfoPanel, flag=flagsL, border=2)
        vbox0.AddSpacer(10)
        #tPwrSZ = self._buildTrainCtrlSizer()
        #vbox0.Add(tPwrSZ, flag=flagsL, border=2)
        self.plcPnls = {}
        plcSZ = self._buildPlcPnlsSizer("PLC Monitor Panels [Trains]", 
                                ('PLC-06', 'PLC-07'))
        vbox0.Add(plcSZ, flag=flagsL, border=2)
        vbox0.AddSpacer(10)
        ctrlSZ = self._buildControlSizer()
        vbox0.Add(ctrlSZ, flag=flagsL, border=2)



        mSizer.Add(vbox0, flag=flagsL, border=2)
        mSizer.AddSpacer(15)
        return mSizer

    def _buildControlSizer(self):
        flagsL = wx.LEFT
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label= "Control Panel")
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        vSizer.Add(label, flag=flagsL, border=2)
        vSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(10, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        caLabel = wx.StaticText(self, label= "> Trains Collision Auto-Avoidance:")
        caLabel.SetFont(font)
        caLabel.SetForegroundColour(wx.Colour("WHITE"))
        hbox1.Add(caLabel, flag=flagsL, border=2)
        hbox1.AddSpacer(10)
        self.caCombo = wx.ComboBox(self,choices = ['Enable', 'Disable']) 
        self.caCombo.SetSelection(0)
        hbox1.Add(self.caCombo, flag=flagsL, border=2)
        self.caCombo.Bind(wx.EVT_COMBOBOX, self.onCombo) 
        vSizer.Add(hbox1, flag=flagsL, border=2)
        return vSizer

    def onCombo(self, event):
        print('---')

    def _buildTrainStateSizer(self):
        flagsL = wx.LEFT
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label="Trains State")
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        vbox0.Add(label, flag=flagsL, border=2)
        vbox0.AddSpacer(5)
        self.trainPnlDict = {}
        for key, panelCfg in gv.gTrackConfig.items():
            self.trainPnlDict[key] = []
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            for i in range(4):
                if i < panelCfg['num']:
                    color = panelCfg['color']
                    trainPanel = pnlFunction.PanelTrain(self, panelCfg['id'], i, 
                                                        bgColor=color,
                                                        fontColor=wx.Colour('WHITE')
                                                        )
                    self.trainPnlDict[key].append(trainPanel)
                    hbox.Add(trainPanel, flag=flagsL, border=2)
                else:
                    img = os.path.join(gv.IMG_FD, 'placeHolder.png')
                    png = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                    placeholder = wx.StaticBitmap(self, -1, png, (0, 0), (png.GetWidth(), png.GetHeight()))
                    hbox.Add(placeholder, flag=flagsL, border=2)
                hbox.AddSpacer(5)
            vbox0.Add(hbox, flag=flagsL, border=2)
            vbox0.AddSpacer(5)
        return vbox0


#--UIFrame---------------------------------------------------------------------
    def _buildTrainCtrlSizer(self):
        flagsL = wx.LEFT
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        vbox0.AddSpacer(5)
        self.speedPanel = pnlFunction.SpeedGuagePanel(self)
        vbox0.Add(self.speedPanel, flag=flagsL, border=2)

        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label="Trains Power Control")
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        vbox0.Add(label, flag=flagsL, border=2)
        vbox0.AddSpacer(5)
        
        for key, panelCfg in gv.gTrackConfig.items():
            img, color = panelCfg['icon'], panelCfg['color']
            if img is None: continue
            img = os.path.join(gv.IMG_FD, img)
            png = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            sublabel = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(sublabel, flag=flagsL, border=2)
            for i in range(panelCfg['num']):
                trainPanel = pnlFunction.PanelTainCtrl(self, panelCfg['id'], i, bgColor=color)
                hbox.Add(trainPanel, flag=flagsL, border=2)
                hbox.AddSpacer(5)
            vbox0.Add(hbox, flag=flagsL, border=2)
            vbox0.AddSpacer(5)
        return vbox0

#--UIFrame---------------------------------------------------------------------
    def _buildPlcPnlsSizer(self, PanelTitle, panelKeySeq):
        flagsL = wx.LEFT
        
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.BOLD)
        label = wx.StaticText(self, label=PanelTitle)
        label.SetFont(font)
        label.SetForegroundColour(wx.Colour("WHITE"))
        vSizer.Add(label, flag=flagsL, border=2)
        vSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        #panelSeq = ('PLC-00', 'PLC-01', 'PLC-02')
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
        # Added the data and time disyplay
        vSizer.AddSpacer(10)
        #timelabel = wx.StaticText(self, label="Date & Time :")
        #timelabel.SetFont(font)
        #timelabel.SetForegroundColour(wx.Colour("WHITE"))

        # Add the train collision auto avoidance 
        vSizer.AddSpacer(10)
        #hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        #collAvoidlabel = wx.StaticText(self, label="Trains collision Auto-avoidance")
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
                for key in self.plcPnls.keys():
                    # update the holding registers
                    tgtPlcID = gv.gPlcPnlInfo[key]['tgt']
                    rsIdx, reIdx = gv.gPlcPnlInfo[key]['hRegsInfo']
                    registList = gv.idataMgr.getPlcHRegsData(tgtPlcID, rsIdx, reIdx)
                    #print(registList)
                    self.plcPnls[key].updateHoldingRegs(registList)
                    csIdx, ceIdx = gv.gPlcPnlInfo[key]['coilsInfo']
                    coilsList = gv.idataMgr.getPlcCoilsData(tgtPlcID, csIdx, ceIdx)
                    #print(coilsList)
                    self.plcPnls[key].updateCoils(coilsList)
                    self.plcPnls[key].updateDisplay()
                # update the display Info
                if gv.iMapMgr:
                    regdataList = gv.idataMgr.getAllPlcRegsData()
                    coildataList = gv.idataMgr.getAllPlcCoisData()
                    for key in gv.gTrackConfig.keys():
                        rsIdx, reIdx = gv.gTrackConfig[key]['trainHregIdx']
                        gv.iMapMgr.updateTrainsSpeed(key, regdataList[rsIdx:reIdx])
                        csIdx, ceIdx = gv.gTrackConfig[key]['trainCoilIdx']
                        gv.iMapMgr.updateTrainsPwr(key, coildataList[csIdx:ceIdx] )
            # Update the train inforation grid.
            if gv.iMapMgr: 
                gv.iInfoPanel.updateTrainInfoGrid()
                self.updateTrainsPanels()
            # update time
            timeStr = 'Date and time : ' + time.strftime(' %Y - %m - %d %H : %M : %S ',time.localtime(time.time()))
            self.timeInfo.SetLabel(timeStr)

#-----------------------------------------------------------------------------
    def updateTrainsPanels(self):

        for key in gv.gTrackConfig.keys():
            trainsInfo = gv.iMapMgr.getTrainsInfo(key)
            for i, data in enumerate(trainsInfo):
                self.trainPnlDict[key][i].updateState(data)

#-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(' If there is any bug, please contact: \n\n \
                        Author:      Yuancheng Liu \n \
                        Email:       liu_yuan_cheng@hotmail.com \n \
                        Created:     2023/07/20 \n \
                        GitHub Link: https://github.com/LiuYuancheng/Metro_emulator \n', 
                    'Help', wx.OK)
        
#-----------------------------------------------------------------------------
    def turnOnallTrainsPwr(self):
        gv.gDebugPrint('Power on all the trains', logType=gv.LOG_INFO)
        self.trainPwrState = [True]*10
        TrainTgtPlcID = gv.PLC_ID
        csIdx, ceIdx = (0, 10)
        if gv.idataMgr:
            for idx in range(csIdx, ceIdx):
                gv.idataMgr.setPlcCoilsData(TrainTgtPlcID, idx, self.trainPwrState[idx])

#-----------------------------------------------------------------------------
    def updatePlcConIndicator(self):
        if gv.idataMgr:
            for val in self.plcPnls.values():
                val.setConnection(gv.idataMgr.getConntionState(gv.PLC_ID))

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
