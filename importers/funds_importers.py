import os
import pandas as pd
from models.models import Asset
from utils.file_processor import FileProcessor, list_files_directory


def import_funds():
  directory = os.path.dirname(os.path.abspath(__file__))
  directory = os.path.join(directory, '..')
  files_dir = list_files_directory(directory, subdirectory='data')
  dataframes = []
  for file_name in files_dir:
    income = pd.read_csv(
      file_name.abs_file_name,
      delimiter=';',
      # delim_whitespace=True,
      index_col=False,
      header=0,
      names = ["real_name","name","segment", 'ticket'],
      encoding='latin-1'
    )
    dataframes.append(income)
    
    # data.append([file_name.date_range, income['Valor líquido'].sum()])
  total = pd.concat(dataframes, ignore_index=True)
  total.drop(['segment'], axis=1, inplace=True)
  total['market'] = 'fi'
  for _, row in total.iterrows():
    data = row.to_dict()
    # print(index, row.to_json())
    Asset.create(**data)

