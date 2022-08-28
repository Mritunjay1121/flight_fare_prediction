from urllib.parse import scheme_chars
from housing.config.configuration import Configuartion
from housing.pipeline.pipeline import Pipeline
from housing.exception import FlightfareException
from housing.logger import logging
from housing.component.data_transformation import DataTransformation
import os,sys
def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuartion(config_file_path=config_path))
        # pipeline=Pipeline()
        # pipeline.run_pipeline()
        pipeline.start()
        logging.info("main function execution completed.")
        # data_validation_config=Configuartion().get_data_transformation_config()
        # print(data_validation_config)
        # scheme_file_path=r"C:\Users\mritu\PycharmProjects\Projects\flight_fare_prediction\config\schema.yaml"
        # file_path=r"C:\Users\mritu\PycharmProjects\Projects\flight_fare_prediction\housing\artifact\data_ingestion\2022-08-19-15-47-07\ingested_data\train\new_train2.csv"


        # df=DataTransformation.load_data(file_path=file_path,schema_file_path=scheme_file_path)
        # print(df.columns)
        # print(df.dtypes)
     

    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()

