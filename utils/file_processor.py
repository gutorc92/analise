import os
import pandas as pd
import re

def list_files_directory(directory, subdirectory = 'transactions'):
  files_dir = os.listdir(os.path.join(directory, subdirectory))
  return [FileProcessor(os.path.join(directory, subdirectory, file_name)) for file_name in files_dir]
       
class DataDirProcesor:
  def __init__(self, file_type: str, directory: str) -> None:
    self.file_type = file_type
    self.directory = directory
    self.files = {
      'fii': 'fundos_listados_imobiliarios.csv',
      'fii-agro': 'fundos_listados_agro.csv' 
    }
  
  def execute(self) -> pd.DataFrame:
    file_name = os.path.join(self.directory, 'data', self.files[self.file_type])
    df = pd.read_csv(
      file_name,
      delimiter=';',
      index_col=False,
      header=0,
      names = ["real_name","name","segment", 'ticket'],
      encoding='latin-1'
    )
    df.drop(['segment'], axis=1, inplace=True)
    df['market'] = self.file_type
    return df
class FileProcessor:

    def __init__(self, file_name) -> None:
       self.directory = os.path.dirname(file_name)
       self.file_name = os.path.splitext(os.path.basename(file_name))[0]
       self.abs_file_name = file_name
       self.date_range = None
       self.convert_file_name_to_date()

    def convert_file_name_to_date(self):
      match = re.search(r'([a-z-A-z_]+)(\d{4})_(\d{2})_(\d{2})_a_(\d{4})_(\d{2})_(\d{2})', self.file_name)
      if not match:
        match = re.search(r'([a-z-A-z\-]+)(\d{4})-(\d{2})-(\d{2})-a-(\d{4})-(\d{2})-(\d{2})', self.file_name)
      if match:
        self.date_range = pd.date_range(start=f'{match.group(2)}-{match.group(3)}-{match.group(4)}',end=f'{match.group(5)}-{match.group(6)}-{match.group(7)}', freq='M')