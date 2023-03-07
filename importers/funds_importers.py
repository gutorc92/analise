import os
import codecs
from models.models import Asset
from utils.file_processor import DataDirProcesor
from peewee import IntegrityError
from bs4 import BeautifulSoup

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

def import_stocks(directory):
  file_name = os.path.join(directory, 'data', 'empresas_listadas.html')
  text = ''
  with codecs.open(file_name, 'r', 'utf-8') as f:
    text = f.read()
  soup = BeautifulSoup(text)
  table = soup.find('table')
  for line in table.find_all("tr"):
    data = {
      'ticket': '',
      'name': '',
      'real_name': '',
      'market': 'stock'
    }
    for index, column in enumerate(line.find_all('td')):
      # print('column', column.find(text=True))
      if index == 0:
        data['ticket'] = column.find(text=True)
      elif index == 1:
        data['name'] = column.find(text=True)
      else:
        break
    # print('data', data)
    try:
      Asset.create(**data)
    except IntegrityError as e:
      print('excpection', e)
