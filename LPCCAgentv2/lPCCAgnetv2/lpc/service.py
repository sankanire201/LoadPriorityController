from typing import Protocol
from messages import MessageType
from messages  import Message
from csv import DictReader, DictWriter
import os
import csv
import collections
from collections import defaultdict
import operator
import numpy as np
class Device(Protocol):
    def connect(self) -> None:
        ...

    def disconnect(self) -> None:
        ...

    def send_message(self, message: Message) -> None:
        ...
    def status_update(self) -> str:
        ...
class LPCmodule(Protocol):

    def set_lpc_control_mode(self,topic:str,message:dict)->None:
        ...
    def read_device_configurations(self,csv_path):
        ...
class WeMoService:
    def register_devices(self,csv_path:str,lpc:LPCmodule):
        lpc.read_device_configurations(csv_path)
        print("registering device")
    def device_status_update(self,topic,message,lpc:LPCmodule):
        lpc.read_device_status(topic,message)
        print("reading devices")
    def device_set_control_mode(self,topic,message,lpc:LPCmodule,devices:Device):
        devicemessage=lpc.set_lpc_control_mode(topic,message)
        devices.send_message(devicemessage)
        #print("setting the conrol mode",devicemessage)


 


