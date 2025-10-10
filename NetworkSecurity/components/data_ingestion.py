from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

##configuration of the Data Ingestion Config

from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifacts_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

#step 1: get the mongo db url from env file
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    """ 
    Read the data from mongo db and export as dataframe
    """
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"],axis=1)
            df.replace(to_replace="na",value=np.nan,inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    """ Store the extracted data into feature store 
    - it takes in the extracted dataframe 
    - creates the feature store file path
    - convert it into csv format & stores that dataframe there
    - returns that dataframe
    """

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_filepath = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_filepath)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_filepath,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    """ Split the data into train and test set """
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    #step 2: Initiate the data ingestion config
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)