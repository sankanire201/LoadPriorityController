from messages import MessageType
from csv import DictReader, DictWriter
import os
import csv
import collections
from collections import defaultdict
import operator
import numpy as np
"""_summary_
This module structures the differnent devices in the LPC structure
Returns:
_type_: _description_
"""
class WeMoPlugDevice:
    """_summary_ class for the WeMo smart plug devices
    """
    def connect(self,csv_path:str) -> None:

        """_summary_ 
        methode to connect to the WeMo smart plug
        """

        

    def disconnect(self) -> None:
        """_summary_
        method to disconnect from the WeMo smart plug
        """
        print("Disconnecting Hue light.")

    def send_message(self, message_type: MessageType, data: str) -> None:
        """_summary_
           method to send commands to the WeMo smart plug
        Args:
            message_type (MessageType): _description_
            data (str): _description_
        """
        print(
            f"Hue light handling message of type {message_type.name} with data [{data}]."
        )

    def status_update(self) -> str:
        """_summary_
        methode to read the status of the WeMo plug

        Returns:
            str: _description_
        """
        return "hue_light_status_ok"


