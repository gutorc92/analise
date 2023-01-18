import os
import pandas as pd
import re
from utils.file_processor import list_files_directory
from models.models import Asset, Transaction
import matplotlib.pyplot as plt
from peewee import fn
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def month_analysis(month, year):
  directory = os.path.dirname(os.path.abspath(__file__))
  directory = os.path.join(directory, '..')
  files_dir = list_files_directory(directory, subdirectory = 'income')
  file_name_analysis = None
  for files_name in files_dir:
    match = re.search(rf'([a-z-A-z_]+){year}_{month:02d}_01_a_{year}_{month:02d}_(30|31|28)', files_name.abs_file_name)
    if match:
      file_name_analysis = files_name.abs_file_name
  income = pd.read_excel(file_name_analysis, decimal=",")
  income['ticket'] = income.apply (lambda row: row['Produto'].split('-')[0].strip()[0:4], axis=1)
  print(income.head())
  fii = []
  drops = []
  for index, row in income.iterrows():
    asset = Asset.get_or_none(Asset.ticket == row['ticket'])
    if not asset:
      drops.append(index)
    else:
      fii.append(asset)
  income.drop(drops, inplace=True)
  income.drop(columns=['Produto', 'Pagamento', 'Tipo de Evento', 'Instituição'], inplace=True)
  # query = Transaction.select(
  #   Transaction.asset,
  #   fn.SUM(Transaction.total).alias('total'),
  #   fn.SUM(Transaction.quantity).alias('quantity')
  # ).group_by(Transaction.asset).where(Transaction.asset.in_(fii),Transaction.status == 'hold')
  query = Asset.select(
    Asset.ticket.alias('ticket'),
    fn.SUM(Transaction.total).alias('total'),
    fn.SUM(Transaction.quantity).alias('quantity')
  ).join(Transaction).group_by(Asset.ticket).where(Transaction.asset.in_(fii),Transaction.status == 'hold').dicts()
  cost = pd.DataFrame.from_dict(query)

  
  # for sample in query:
    # print(f"asset: {sample['ticket']}, total: {sample['total']}")
    # print(f'quantity: {sample.quantity}, mean: {sample.total/sample.quantity}')
  print(income.columns)
  income = income.groupby('ticket')['Quantidade', 'Valor líquido'].sum()
  print(income.head())
  # income.set_index('ticket', inplace=True)
  
  cost.set_index('ticket', inplace=True)
  result = pd.concat([income, cost], axis=1, join="inner" )
  result['median_price'] = result.apply(lambda row: (row['total'] / row['quantity']), axis=1)
  result['d/y'] = result.apply(lambda row: (row['Valor líquido'] / row['total'])*100, axis=1)
  print(result.head())
  result.plot.pie(y='Valor líquido', figsize=(8, 8), autopct='%1.1f%%',)
  plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
  # plt.tight_layout()
  plt.savefig(f"pie_chart_{month:02d}_{year}.png")
  result.plot.bar(y='d/y', rot=90)
  plt.savefig(f"bar_chart_{month:02d}_{year}.png")