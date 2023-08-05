import os
import logging
import pickle
import pandas as pd
import base64
import ast

from io import BytesIO, StringIO
from datetime import date
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob._models import BlobType
from catboost import CatBoostClassifier

logger = logging.getLogger(__name__)

def download_dataframe(container, blob, connection_string):
    """
    Downloads string with serialized pickled dataframe from Azure Blob Storage,
    deserialize it and return the dataframe.

    :param container: Name of container
    :type data: str
    :param blob: Name of blob
    :type data: str
    :param connection_string: Connection string to Azure Storage
    :type container_string: str
    :return: Dataframes containing data from total soundings, CPTs, ground samples, and interpretations, respectively.
    :rtype: pd.DataFrame
    """

    service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = service_client.get_blob_client(container = container, blob = blob)

    try:  
        stream = blob_client.download_blob()
        data = stream.readall()
        dataframe = _deserialize_csv_blob_data(data)
    except Exception:
        logger.error(f"Cannot download blob {blob}", exc_info=True)

    logger.info(f"Downloaded blob {blob}")

    return dataframe

def download_unprocessed_dataframes(container, connection_string, include_processed = False):
    """
    Downloads strings with serialized dataframes from Azure Blob Storage,
    deserialize them and return a tuple of dataframes grouped by type of data.
    The check for processed data uses metadata defined on the blobs.
    
    :param container: Name of container where blobs are located
    :type container: str
    :param connection_string: Connection string to Azure Storage
    :type container_string: str
    :param include_processed: Include data that has been flagged as processed
    :type include_processed: bool
    :return: List of dataframes containing data from total soundings, CPTs, ground samples, and interpretations, respectively.
    :rtype: tuple of list
    """
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container = service_client.get_container_client(container)

    blob_list = container.list_blobs(include="metadata")

    tot, cpt, prv, tlk = [], [], [], []

    for blob in blob_list:
        metadata = blob.metadata
        if not metadata or (not include_processed and metadata.get("Processed") == "1"):
            continue

        try:  
            blob_client = container.get_blob_client(blob = blob.name)
            stream = blob_client.download_blob()
            data = stream.readall()

            if metadata.get("DataFormat") == "csv":
                dataframe = _deserialize_csv_blob_data(data)
            elif metadata.get("DataFormat") == "pl":
                dataframe = _deserialize_pickled_blob_data(data)
            else:
                raise ValueError("Argument data_format only accepts 'csv' or 'pl'")

            if metadata.get("Type") == "tot":
                tot.append(dataframe)
            elif metadata.get("Type") == "cpt":
                cpt.append(dataframe)
            elif metadata.get("Type") == "tlk":
                tlk.append(dataframe)
            elif metadata.get("Type") == "prv":
                prv.append(dataframe)
 
            metadata["Processed"] = "1"
            blob_client.set_blob_metadata(metadata)

        except Exception:
            logger.error(f"Cannot download blob {blob.name}", exc_info=True)

        logger.info(f"Downloaded blob {blob.name}")

    tot = merge_dfs(tot) if len(tot) > 0 else None
    cpt = merge_dfs(cpt) if len(cpt) > 0 else None
    prv = merge_dfs(prv) if len(prv) > 0 else None
    tlk = merge_dfs(tlk, sort_by=["id", "kote"]) if len(tlk) > 0 else None

    return tot, cpt, prv, tlk

def upload_dataframe_to_blob_storage(
    dataframe: pd.DataFrame, blob_name, container_name, 
    connection_string, metadata=None, 
    data_format="csv", blob_type=BlobType.BlockBlob):
    """
    Upload serialized dataframe to Azure Blob storage.

    :param dataframe: Dataframe with soundingdata
    :type dataframe: Pandas dataframe
    :param blob_name: Name of blob
    :type data: str
    :param container_name: Name of container
    :type data: str
    :param connection_string: Connection string to Azure Storage
    :type container_string: str
    :param metadata: Metadata to set on blob
    :type data: dict
    :param data_format: Determines whether to use pickle to serialize dataframe or to use csv. 
    Accepted inputs are {"csv","pl"}
    :type source: str
    :param blob_type: Defines type of blob. Usually either BlockBlob are AppendBlob
    :type blob_type: azure.storage.blob._models.BlobType
    """

    if dataframe is None:
        return 0
    
    uploaded = 0

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        if data_format == "csv":
            serialized_data = dataframe.to_csv()
        elif data_format == "pl":
            serialized_data = _pickle_dataframe(dataframe)
        else:
            raise ValueError("Argument data_format only accepts 'csv' or 'pl'")

        container_client.upload_blob(name = blob_name, data = serialized_data, blob_type = blob_type)        

        if metadata:
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.set_blob_metadata(metadata)

        uploaded = len(dataframe)
    except Exception:
        logger.error("Uploading dataframe to Blob Storage failed", exc_info=True)

    return uploaded

def _pickle_dataframe(dataframe):
    """
    Serialize dataframe to byte string by using pickle

    :param dataframe: Dataframe with soundingdata
    :type dataframe: Pandas dataframe
    :return: Serialized dataframe
    :rtype: str
    """

    bytes_output = BytesIO()
    pickle.dump(dataframe, bytes_output)
    pickle_data = base64.b64encode(bytes_output.getvalue()).decode()
    bytes_output.close()

    return pickle_data

def _deserialize_pickled_blob_data(bytestring):
    """
    Deserialize byte string from Azure Blob Storage into Pandas dataframe

    :param bytestring: String containing pickled dataframes serialized in bytes
    :type bytestring: str
    :return: Dataframes containing data from total soundings, CPTs, ground samples, and interpretations, respectively.
    :rtype: tuple of pd.DataFrame
    """
    pickle_bytes = BytesIO(base64.b64decode(bytestring))
    dataframe = pickle.loads(pickle_bytes.read())
    pickle_bytes.close()

    return dataframe

def _deserialize_csv_blob_data(csv_bytestring):
    """
    Deserialize byte string of csv-file from Azure Blob Storage into Pandas dataframe

    :param bytestring: String of bytes containing dataframes in csv-format
    :type bytestring: str
    :return: Dataframes containing data from total soundings, CPTs, ground samples, and interpretations, respectively.
    :rtype: tuple of pd.DataFrame
    """

    buffer = StringIO(csv_bytestring.decode('utf-8'))

    dataframe = pd.read_csv(buffer)

    return dataframe

def save_new_CatBoostClassifier_model(model: CatBoostClassifier, container, blob, connection_string):
    """
    Save new CatboostClassifier to Blob Storage and set this model to
    be the active model.

    :param model: Trained CatboostClassifier
    :type model: CatBoostClassifier
    """

    model_name = f"model_{date.today()}.cbm"

    service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = service_client.get_container_client(container)

    _set_exisiting_models_inactive(service_client, container_client)

    filepath = _save_model_locally(model, model_name)

    with open(filepath, "rb") as file:
        container_client.upload_blob(name=model_name, data=file.read())

    _set_model_metadata(container_client, model_name)

def _set_model_metadata(container, blob_name):
    """
    Set metadata on new model. The property 'Active' defines
    which model will be used in production. The new model will be
    set as the active model.
    """
    metadata = {
        "Active": "1"
    }

    blob_client = container.get_blob_client(blob_name)
    blob_client.set_blob_metadata(metadata)

def _set_exisiting_models_inactive(service_client, container_client):
    """
    Set all exisiting models to inactive. The property 'Active' defines
    which model will be used in production.
    """
    blob_list = container_client.list_blobs(include="metadata")

    for blob in blob_list:
        if blob.metadata:
            blob_client = container_client.get_blob_client(blob = blob.name)

            new_metadata = blob.metadata
            new_metadata["Active"] = "0"

            blob_client.set_blob_metadata(new_metadata)

def _save_model_locally(model, model_name):
    """
    Save model to 'models'-folder
    """
    model_folder = f"models"

    if not os.path.exists(model_folder):
        os.mkdir(model_folder)

    filepath = os.path.join(model_folder, model_name)
    
    model.save_model(filepath)

    return filepath

def get_active_model(container, connection_string):
    """
    Downloads the active model which is used in production.
    """
    service_client = BlobServiceClient.from_connection_string(connection_string)
    container = service_client.get_container_client(container)

    blob_list = container.list_blobs(include="metadata")

    for blob in blob_list:
        if blob.metadata and blob.metadata.get("Active") == "1":
            blob_client = container.get_blob_client(blob.name)
            stream = blob_client.download_blob()
            data = stream.readall()

            return CatBoostClassifier().load_model(blob=data)
    
    return None

def merge_dfs(dfs, reset_index=True, sort_by=["id", "dybde"]):
    """
    Combine a list of dataframes into a single dataframe with fixed indices and sorted rows.

    :param dfs: Dataframes to concatenate
    :type dfs: list of pd.DataFrame
    :param reset_index: Reset the index of the concatenated DataFrame?
    :type reset_index: bool
    :param sort_by: parameter passed to df.sort_values
    :type sort_by: str | list of str
    :return: Concatenated dataframe
    :rtype: pd.DataFrame
    """
    df = pd.concat(dfs, sort=False)
    if reset_index:
        df.reset_index(drop=True, inplace=True)
    df.sort_values(by=sort_by, inplace=True)
    return df