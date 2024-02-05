# Railway[Metro] IT/OT System Cyber Security Test Platform ( mini cyber range)

**Project Design :** We aim to develop a simplified and straightforward digital twin-style emulation platform for a railway system, simulating the operations of multiple trains on various tracks, each with distinct sensor-signal controls. This platform serves as an invaluable tool for cyber security researchers to showcase and test the impact of various IT attacks on OT systems. The system comprises two sub-projects(cyber range) with eight primary components :

**Railway Company IT-network Cyber Range**

This IT network cyber range project will simulate the normal cooperation network of the railway company, we will use the Custer User Emulation system to automate simulate different staff's daily work such as IT-Support-Engineer, Officer Staff, Railway HQ operator, Train driver / safety checker. The main components includes: 

- Railway company cooperation network environment (virtual hardware: computer,  node, firewall, router, switches)
- Railway company staff activities auto generator (virtual staff: IT-Support-Engineer, Officer Staff, Railway HQ operator, Train driver / safety checker)

**Railway System OT Cyber Range**

The OT Cyber range will enumerate all the railway system's supervision SCADA network, the OT-production network and the physical real-world.  The main components includes: 

- 2D Railway[Metro] System Real-world Emulator
- Railway System SCADA HMI
- Railway System Trains Controller HMI
- Railway Junctions Sensor-Signal System Control PLC Simulator
- Railway Stations Sensor-Signal System Control PLC Simulator
- Railway Trains Sensor-Power System Control PLC Simulator

##### Project Use Case

We are glad to share that the Railway [Metro] IT/OT Emulation System Cyber Security Test Platform we developed this year was used for building one part of the cyber-attack target training system in the NATO CCDCOE Cross Sword 2023 offensive cyber exercise. CCDCOE LinkedIn POST: [ > link](https://www.linkedin.com/posts/natoccdcoe_crossedswords-activity-7140986334961217536-7dM5/?utm_source=share&utm_medium=member_desktop)

![](doc/img/linkedinpost2.png)

[TOC]

**Table of Contents**

- [Railway[Metro] IT/OT System Cyber Security Test Platform ( mini cyber range)](#railway-metro--it-ot-system-cyber-security-test-platform---mini-cyber-range-)
        * [Project Use Case](#project-use-case)
    + [Introduction](#introduction)
    + [Detailed Sub-System Design](#detailed-sub-system-design)
      - [1. 2D Railway[Metro] System Real-world Emulator](#1-2d-railway-metro--system-real-world-emulator)
      - [2. Railway System SCADA HMI](#2-railway-system-scada-hmi)
      - [3. Railway System Trains Controller HMI](#3-railway-system-trains-controller-hmi)
      - [4. Railway Junctions Sensor-Signal System Control PLC Simulator](#4-railway-junctions-sensor-signal-system-control-plc-simulator)
      - [5. Railway Stations Sensor-Signal System Control PLC Simulator](#5-railway-stations-sensor-signal-system-control-plc-simulator)
      - [6. Railway Trains Sensor-Power System Control PLC Simulator](#6-railway-trains-sensor-power-system-control-plc-simulator)
    + [System Network Design](#system-network-design)
      - [Main cyber range network design](#main-cyber-range-network-design)
      - [OT cyber range network design](#ot-cyber-range-network-design)
    + [Cyber Attack Demonstration Case Study](#cyber-attack-demonstration-case-study)
      - [IT system cyber attack case study](#it-system-cyber-attack-case-study)
        * [IT system cyber attack case 1: Phishing and backdoor trojan](#it-system-cyber-attack-case-1--phishing-and-backdoor-trojan)
      - [OT system cyber attack case study](#ot-system-cyber-attack-case-study)
        * [OT Cyber Attack Demo on PLC [Case Study 01] : False Data / Cmd Injection Attack Case](#ot-cyber-attack-demo-on-plc--case-study-01----false-data---cmd-injection-attack-case)
        * [OT Cyber Attack Demo on HMI  [Case Study 02] : ARP Spoofing Attack Case](#ot-cyber-attack-demo-on-hmi---case-study-02----arp-spoofing-attack-case)
        * [OT Cyber Attack Demo on PLC [ Case Study 03 ] : DDoS Attack Case](#ot-cyber-attack-demo-on-plc---case-study-03-----ddos-attack-case)
        * [OT Cyber Attack Demo on HMI-PLC control Chain [ Case Study 04 ] : Man in the middle Attack Case](#ot-cyber-attack-demo-on-hmi-plc-control-chain---case-study-04-----man-in-the-middle-attack-case)
      - [Problem and Solution](#problem-and-solution)

------

### Introduction 

The Railway[Metro] IT/OT System Security Test Platform serves as a miniature railway IT/OT network emulation system, designed to empower ICS researchers in testing their IT/OT attack and defense solutions on our cyber range. Additionally, it also provides different IT/OT cyber attack cases for the ICS security training and education purposes. The entire system is composed of four main network components, as illustrated in the diagram below:

![](doc/img/Components.png)

1. **Cooperate network**: This subnet replicates a typical railway company's corporate IT network, encompassing various functional servers (email, DMZ, staff management) and a production management workstation. This workstation hosts essential components such as the production log archiving database, internal document server, and operator manuals.
2. **Supervision SCADA network**: Simulating the SCADA system network, this subnet features distinct SCADA data/historian servers, multiple HMI computers for system operators, and maintenance computers dedicated to ICS/OT-system engineers.
3. **Production network**: This subnet houses diverse PLC simulator programs, contributing to a realistic representation of the production environment within the railway system.
4. **Physical real-world emulation network**: In this subnet, railway real-world components are emulated to demonstrate the tangible effects of actual items in the real working environment.

Railway[Metro] **OT** System security mini cyber range is constructed by six main components (introduced in the program design) under below structure: 

![](doc/img/networkCommDesign.png)

Railway[Metro] **IT** System security mini cyber range is constructed by 5 main sub-network (introduced in the program design) under below structure: 

![](attack/img/topology.png)



`Version v0.3.1`

------

### Detailed Sub-System Design

The detail introduction of each component is shown below: 

#### 1. 2D Railway[Metro] System Real-world Emulator

2D Railway[Metro] System real-world emulator UI: 

![](doc/video/connectionHub5.gif)

2D Railway[Metro] System real-world emulator UI detailed software design document: [ > link](doc/metroEmuUI_readme.md)



#### 2. Railway System SCADA HMI

Railway System SCADA HMI UI :

![](doc/video/scadaHmi.gif)

Railway System SCADA HMI detailed software design document: [> link](doc/scadaHMI_readme.md)



#### 3. Railway System Trains Controller HMI

Railway System Trains Controller HMI UI

![](doc/video/trainHMIhalf.gif)

Railway System Trains Controller HMI detailed software design document: [> link](doc/trainsCtrlHMI.md)



#### 4. Railway Junctions Sensor-Signal System Control PLC Simulator

PLCs set Digital I/O connection and the Ladder logic:

![](doc/img/signalPlc.png)

Railway Junctions Sensor-Signal System Control PLC Simulator detailed software design document: [ > link](doc/sensorsPLCSimu_readme.md)



#### 5. Railway Stations Sensor-Signal System Control PLC Simulator

PLCs set Digital I/O connection and the Ladder logic:

![](doc/img/stationPlc.png)

Railway Stations Sensor-Signal System Control PLC Simulator detailed software design document: [> link](doc/stationPLCSimu_readme.md)



#### 6. Railway Trains Sensor-Power System Control PLC Simulator

PLCs set Digital I/O connection and the Ladder logic:

![](doc/img/trainPlc.png)

Railway Trains Sensor-Power System Control PLC Simulator detailed software design document: [link](doc/trainsPlcSimu_readme.md)



**Program version:** `v0.3.2`

Code base: https://github.com/LiuYuancheng/Metro_emulator/tree/main/src

------

### System Network Design 

#### Main cyber range network design

![](doc/img/network_mapping.png)

#### OT cyber range network design

![](doc/img/networkDesign.png)



------

### Cyber Attack Demonstration Case Study

Currently we use our mini cyber range provide one IT cyber attack case study and four different OT cyber attack case study. 

#### IT system cyber attack case study

##### IT system cyber attack case 1: Phishing and backdoor trojan 

![](doc/img/attackRoadMap.png)

Detailed case study document [> link](https://github.com/LiuYuancheng/Cross-Sword-2023-Nato-Event/blob/main/attackDemos/falseDataInjection/instructorManual_FDJ.md)

#### OT system cyber attack case study

##### OT Cyber Attack Demo on PLC [Case Study 01] : False Data / Cmd Injection Attack Case

![](attack/img/falseCmdInjection.png)

Detailed case study document [> link](attack/OT_attack_case1_falseCmdInjection.md)

##### OT Cyber Attack Demo on HMI  [Case Study 02] : ARP Spoofing Attack Case

![](attack/img/ArpSpoofing/arpspoofing.png)

Detailed case study document [> link](attack/OT_attack_case2_arpSpoofingAttack.md)

##### OT Cyber Attack Demo on PLC [ Case Study 03 ] : DDoS Attack Case

![](attack/img/ddos/ddosAtkRoadmap.png)

Detailed case study document [> link](attack/OT_attack_case3_ddosModbusAttack.md)

##### OT Cyber Attack Demo on HMI-PLC control Chain [ Case Study 04 ] : Man in the middle Attack Case

![](attack/img/mitm/attackRoadmap.png)

Detailed case study document [> link](attack/OT_attack_case4_MitmAttack.md)



------

#### Problem and Solution

Refer to `doc/ProblemAndSolution.md`



------

> last edit by LiuYuancheng (liu_yuan_cheng@hotmail.com) by 30/05/2023 if you have any problem, please send me a message. 