# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

""" Library of code for telemetry logs reused across various calling features """
from datetime import datetime
from enum import Enum
import logging
import time
import traceback
from azure.cosmos import CosmosClient, PartitionKey

class TelemetryType(Enum):
    """ Enum for type of telemetry """
    CHAT = "Chat Entry"
    CHAT_ERROR = "Chat Entry Error"

class TelemetryLog:
    """ Class for logging status of various processes to Cosmos DB"""

    def __init__(self, url, azure_credential, database_name, container_name):
        """ Constructor function """
        self._url = url
        self.azure_credential = azure_credential
        self._database_name = database_name
        self._container_name = container_name
        self.cosmos_client = CosmosClient(url=self._url, credential=self.azure_credential, consistency_level='Session')
        self._log_document = {}

        # Select a database (will create it if it doesn't exist)
        self.database = self.cosmos_client.get_database_client(self._database_name)
        if self._database_name not in [db['id'] for db in self.cosmos_client.list_databases()]:
            self.database = self.cosmos_client.create_database(self._database_name)

        # Select a container (will create it if it doesn't exist)
        self.container = self.database.get_container_client(self._container_name)
        if self._container_name not in [container['id'] for container
                                        in self.database.list_containers()]:
            self.container = self.database.create_container(id=self._container_name,
                partition_key=PartitionKey(path="/sessionID"))

    def record_telemetry(self, telemetry_type:TelemetryType, session_id:str, chat_start_time:time, error_message:str):
        """
        Records telemetry data for a given session.

        Args:
            telemetry_type (str): The type of telemetry to be recorded.
            session_id (str): The unique identifier for the session.
            chat_start_time (time): The start time of the chat session in seconds since the epoch.
            error_message (str): The error message to be logged, if any.

        Raises:
            Exception: If there is an error in recording telemetry, it logs the error and stack trace.
        """
        try:
            current_time = datetime.now()
            end_time = time.time()
            response_time = end_time - chat_start_time
            log_entry = {
                'id': current_time.isoformat() + "-" + session_id,
                'datetime': current_time.strftime("%Y-%m-%d %H:%M:%S"),
                'telemetry_type': telemetry_type.value,  # Convert to string
                'sessionID': session_id,
                'response_time': response_time,
                'error': error_message
            }
            self.container.create_item(body=log_entry)
        except Exception as e:
            logging.error("Error in recording telemetry: %s", e)
            logging.error(traceback.format_exc())
