import sys
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
import certifi
from pathlib import Path  # corrected import

from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join(artifact_folder)


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()

    def export_collection_as_dataframe(self, collection_name: str, db_name: str) -> pd.DataFrame:
        try:
            # Secure MongoDB connection with TLS CA bundle
            mongo_client = MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            collection = mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def export_data_into_feature_store_file_path(self) -> str:
        try:
            logging.info(f"Exporting data from MongoDB")
            raw_file_path = self.data_ingestion_config.artifact_folder

            os.makedirs(raw_file_path, exist_ok=True)

            sensor_data = self.export_collection_as_dataframe(
                collection_name=MONGO_COLLECTION_NAME,
                db_name=MONGO_DATABASE_NAME
            )

            logging.info(f"Saving exported data to feature store path: {raw_file_path}")

            feature_store_file_path = os.path.join(raw_file_path, 'wafer_fault.csv')
            sensor_data.to_csv(feature_store_file_path, index=False)

            return feature_store_file_path

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> Path:
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")

        try:
            feature_store_file_path = self.export_data_into_feature_store_file_path()
            logging.info("Data fetched and saved from MongoDB")

            logging.info("Exiting initiate_data_ingestion method of DataIngestion class")

            return Path(feature_store_file_path)

        except Exception as e:
            raise CustomException(e, sys) from e
