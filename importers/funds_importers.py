import os
import pandas as pd
from models.models import Asset
from utils.file_processor import DataDirProcesor


def import_funds(directory):
  data_processor = DataDirProcesor('fi', directory)
  total = data_processor.execute()
  for _, row in total.iterrows():
    data = row.to_dict()
    # print(index, row.to_json())
    Asset.create(**data)
  data_processor = DataDirProcesor('fii-agro', directory)
  total = data_processor.execute()
  for _, row in total.iterrows():
    data = row.to_dict()
    # print(index, row.to_json())
    Asset.create(**data)

