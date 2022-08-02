from tkinter import E
from housing.config.configuration import Configuartion
from housing.logger import logging
from housing.exception import FlightfareException
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.config_entity import DataIngestionConfig
from housing.component.data_ingestion import DataIngestion
# from housing.component.data_validation import DataValidation
# from housing.component.data_transformation import DataTransformation
# from housing.component.model_trainer import ModelTrainer
# from housing.component.model_evaluation import ModelEvaluation
# from housing.component.model_pusher import ModelPusher
import os,sys


class Pipeline:

    def __init__(self,config:Configuartion=Configuartion()) -> None:
        try:
            self.config=config

        except Exception as e:

            raise FlightfareException(e,sys) from e

    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            # data_ingestion.initiate_data_ingestion()
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise FlightfareException(e, sys) from e


    def start_data_validation(self):
        pass

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
        pass

    
    def start_model_evaluation(self):
        pass

    
    def start_model_pusher(self):
        pass
    def run_pipeline(self):
        try:
           
            # data ingestion
            data_ingestion_artifact=self.start_data_ingestion()
            logging.info("Pipeline starting.")
        except Exception as e:
            raise FlightfareException(e,sys) from e 


            