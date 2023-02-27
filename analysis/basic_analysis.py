import os
import pandas as pd
import re
from utils.file_processor import FileIncomeProcessor
from models.models import Asset, Transaction
import matplotlib.pyplot as plt
from peewee import fn
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def month_analysis(month, year, directory):
  file_processor = FileIncomeProcessor(month, year, directory)
  income = pd.read_excel(file_processor.find_file(), decimal=",")
  income['ticket'] = income.apply (lambda row: row['Produto'].split('-')[0].strip()[0:4], axis=1)
  assets = [ asset for asset in Asset.select().where(Asset.ticket.in_(income['ticket'].to_list()))]
  income.drop(columns=['Produto', 'Pagamento', 'Tipo de Evento', 'Instituição'], inplace=True)
  query = Asset.select(
    Asset.ticket.alias('ticket'),
    fn.SUM(Transaction.total).alias('total'),
    fn.SUM(Transaction.quantity).alias('quantity')
  ).join(Transaction).group_by(Asset.ticket).where(Transaction.asset.in_(assets),Transaction.status == 'hold').dicts()
  
  cost = pd.DataFrame.from_dict(query)
  print('cost')
  print(cost)
  income = income.groupby('ticket')['Quantidade', 'Valor líquido'].sum()
  
  cost.set_index('ticket', inplace=True)
  result = pd.concat([income, cost], axis=1, join="inner" )
  result['median_price'] = result.apply(lambda row: (row['total'] / row['quantity']), axis=1)
  result['d/y'] = result.apply(lambda row: (row['Valor líquido'] / row['total'])*100, axis=1)
  print(result)
  result.plot.pie(y='Valor líquido', figsize=(8, 8), autopct='%1.1f%%',)
  plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
  # plt.tight_layout()
  plt.savefig(f"pie_chart_{month:02d}_{year}.png")
  result.plot.bar(y='d/y', rot=90)
  plt.savefig(f"bar_chart_{month:02d}_{year}.png")