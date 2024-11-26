# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

""" Library of code for conversation logs reused across various calling features """
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey

class ConversationLog:
    """ Class for logging conversation history to Cosmos DB"""

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

    def log_conversation(self, session_id:str, question:str, model_response:str, model_response_time:any, feedback:str, feedback_comment:str, error_flag:any):
        """
        Records telemetry data for a given session.

        Args:

        Raises:
            Exception: If there is an error in recording telemetry, it logs the error and stack trace.
        """
        current_time = datetime.now()
        record_id = current_time.isoformat() + "-" + session_id
        log_entry = {
            'id': record_id,
            'datetime': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'sessionID': session_id,
            'user_input': question,
            'model_response': model_response,
            'model_response_time': model_response_time,
            'feedback': feedback,
            'feedback_comment': feedback_comment,
            'error_flag': error_flag
        }
        self.container.create_item(body=log_entry)
        return record_id
