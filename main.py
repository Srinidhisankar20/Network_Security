from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
from NetworkSecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("Data Ingestion started")
        trainingpipelineconfig = TrainingPipelineConfig()
        #Data Ingestion
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(data_ingestion_artifact)
        #Data Validation
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)
        
        

    except Exception as e:
        raise NetworkSecurityException(e, sys)