import pandas as pd
from models.models import Asset
from utils.file_processor import DataDirProcesor
from peewee import IntegrityError


def import_funds(directory, asset_types):
  for type_fund in asset_types:
    data_processor = DataDirProcesor(type_fund, directory)
    total = data_processor.execute()
    for _, row in total.iterrows():
      data = row.to_dict()
      # print(index, row.to_json())
      try:
        Asset.create(**data)
      except IntegrityError as e:
        pass

