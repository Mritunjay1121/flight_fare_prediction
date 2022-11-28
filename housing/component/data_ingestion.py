from housing.entity.config_entity import DataIngestionConfig
import sys,os
from housing.exception import FlightfareException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import tarfile
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        # print(data_ingestion_config,"sfs") 
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config
    
        except Exception as e:
            raise FlightfareException(e,sys)
 


    def download_housing_data(self) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url
            

            #folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)
            os.makedirs(tgz_download_dir,exist_ok=True)

            flighfare_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir, flighfare_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"File :[{tgz_file_path}] has been downloaded successfully.")
            return tgz_file_path

        except Exception as e:
            raise FlightfareException(e,sys) from e 

    def extract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                
                import os
                
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(housing_tgz_file_obj, path=raw_data_dir)
            logging.info(f"Extraction completed")

        except Exception as e:
            raise FlightfareException(e,sys) from e
    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            # print(raw_data_dir,1)

            file_name = os.listdir(raw_data_dir)[0]
            # print(file_name,2)
            flightfare_file_path = os.path.join(raw_data_dir,file_name)
            # print(flightfare_file_path,3)
             
            # Suppose our training dataset has a specific spread of fare price and with specifc data stats then we'll ensure that those stast will also be present in test dataset this is called as Stratified Dataset Split 

            logging.info(f"Reading excel file: [{flightfare_file_path}]")
            flightfare_data_frame = pd.read_csv(flightfare_file_path)

            # flightfare_data_frame["flightfare_cat"] = pd.cut(
            #     flightfare_data_frame["median_income"],
            #     bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
            #     labels=[1,2,3,4,5]
            # )
            x=flightfare_data_frame.drop("Price",axis=1)
            y=flightfare_data_frame['Price']
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
            train_set=pd.concat([x_train, y_train], axis=1)
            test_set=pd.concat([x_test, y_test], axis=1)


            logging.info(f"Splitting data into train and test")
            # strat_train_set = None
            # strat_test_set = None

            # split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            # for train_index,test_index in split.split(flightfare_data_frame, flightfare_data_frame["flightfare_cat"]):
            #     strat_train_set = flightfare_data_frame.loc[train_index].drop(["flightfare_cat"],axis=1)
            #     strat_test_set = flightfare_data_frame.loc[test_index].drop(["flightfare_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)
            # print(train_file_path,4)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            # print(test_file_path,5)
            # if strat_train_set is not None:
            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            #     logging.info(f"Exporting training datset to file: [{train_file_path}]")
            #     strat_train_set.to_csv(train_file_path,index=False)
                # print(strat_test_set,6)
            train_set.to_csv(train_file_path,index=False)
            # if strat_test_set is not None:
            os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
            #     logging.info(f"Exporting test dataset to file: [{test_file_path}]")
            #     strat_test_set.to_csv(test_file_path,index=False)
            #     # print(strat_test_set,7)
            test_set.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact
        except Exception as e:
            raise FlightfareException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path =  self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise FlightfareException(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")