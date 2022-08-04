from housing.config.configuration import Configuartion
from housing.pipeline.pipeline import Pipeline
from housing.exception import FlightfareException
from housing.logger import logging


def main():
    try:

        pipeline=Pipeline()
        pipeline.run_pipeline()
        # data_validation_config=Configuartion().get_data_validation_config()
        # print(data_validation_config)

    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()

