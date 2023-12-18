from typing import Protocol
from diagonstic import DiagnosticsSource
from devices import WeMoPlugDevice
from csv import DictReader, DictWriter
import os
import csv
import collections
from collections import defaultdict
import operator
import numpy as np
class LPCmodule(Protocol):

    def set_lpc_control_mode(self,topic:str,message:dict)->None:
        ...
    def read_device_configurations(self,csv_path):
        ...
    def read_device_status(self,topic,message):
        ...
class LPCWeMo(LPCmodule):
    def __init__(self):
        self.__WeMo_Actual_Status={}
        self.__WeMo_Priorities=defaultdict(list)
        self.__WeMo_Power_Consumption_Sql={}
        self.__WeMo_Topics={}
        self.__WeMo_Consumption={}
        self.__WeMo_cc={}
        self.__WeMo_Priority_increment={}
        self.__loads_consumption={}
        self.__loads_max_consumption={}
        self.__buildings={}
        self.__WeMo_respond_list={}
        self.__total_consumption=0
        self.__control_command=0
        self.__Power_Consumption_Upper_limit=1000000
        self.__controller_mode='None'
        self.__controller_mode_active='Inactive'
        self.__building_Controller=""

    def set_lpc_control_mode(self,topic,message):
        result = str(topic).find('control')
        if result >=0:
            result=topic.find('shedding')
            if result >=0:
                self.__control_command=int(message)
                self.__controller_mode_active='Active'
                self.__controller_mode='Shedding'
               # self.lpc_shedding(message)
                self.__controller_mode_active='Inactive'
            result=topic.find('directcontrol')
            if result >=0:
                self.__control_command=int(message[1])
                self.__controller_mode_active='Active'
                self.__controller_mode='Direct'
                #self.lpc_directcontrol(message)
                self.__controller_mode_active='Inactive'
            result=topic.find('increment')
            if result >=0:
                self.__control_command=int(message)
                self.__controller_mode_active='Active'
                self.__controller_mode='Increment'
                #self.lpc_increment(message)
                self.__controller_mode_active='Inactive'

    def read_device_configurations(self,csv_path):
       if os.path.isfile(csv_path):
              with open(csv_path, "r") as csv_device:
                reader = DictReader(csv_device)         
         #iterate over the line of the csv
                noofbuilding={}
                for point in reader:
                    Name = point.get("Name")
                    Priority = point.get("Priority")
                    Topic = point.get("Topic")
                    Cluster_Controller = point.get("cc")
                    self.__building_Controller=Cluster_Controller
                    Consumption = point.get("Consumption")
                    if Name=='\t\t\t':
                         pass
                    else:
                        Name=Name+"_"+Cluster_Controller
                        self.__WeMo_Actual_Status[Topic]=0
                        self.__WeMo_Priorities[int(Priority)].append([Topic,int(Consumption)])
                       # self.__WeMo_Topics[Name]=self.__topic+Cluster_Controller+"/"+Name
                        self.__WeMo_Consumption[Topic]=Consumption
                        #self.__WeMo_cc[Name]=Cluster_Controller
                        self.__WeMo_Power_Consumption_Sql[Topic]=0
                        self.__loads_max_consumption[Topic]=0
                        self.__loads_consumption[Topic]=0
                        self.__WeMo_Priority_increment[Topic]=int(Priority)
                        #self.__buildings[Building]=0 
                print(self.__WeMo_Priority_increment)
       else:
            # Device hasn't been created, or the path to this device is incorrect
            raise RuntimeError("CSV device at {} does not exist".format(self.csv_path))
    def read_device_status(self,topic,message):
        result=0
        print('*********************************************** Topic *******************************',topic)
        result = topic.find('NIRE_WeMo_cc_1')
        
        if result >=0:
            result=0
            
            result = topic.find('control')
            if result >=0:
                    pass
            else:
                load_tag=topic.split("/all")
       #     index=load_tag[-2]+"_"+load_tag[-3][-1]
                self.__loads_consumption[load_tag[0]]=int((message[0])['power'])/1000
                print(self.__loads_consumption[load_tag[0]],'hah')
                self.__WeMo_Actual_Status[load_tag[0]]=int((message[0])['status'])
                self.__WeMo_Priority_increment[load_tag[0]]=int((message[0])['priority'])
                if self.__loads_max_consumption[load_tag[0]]< self.__loads_consumption[load_tag[0]]:
                    self.__loads_max_consumption[load_tag[0]]=self.__loads_consumption[load_tag[0]]
                self.__total_consumption=sum(self.__loads_consumption.values())