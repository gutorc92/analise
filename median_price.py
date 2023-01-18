import os
import matplotlib.pyplot as plt
import pandas as pd
from file_processor import FileProcessor

      

def list_files_directory(directory, subdirectory = 'transactions'):
  files_dir = os.listdir(os.path.join(directory, subdirectory))
  return [FileProcessor(os.path.join(directory, subdirectory, file_name)) for file_name in files_dir]

directory = os.path.dirname(os.path.abspath(__file__))
files_dir = list_files_directory(directory)
dataframes = []
for file_name in files_dir:
  income = pd.read_excel(file_name.abs_file_name, decimal=",")
  # income['ticket'] = income.apply (lambda row: row['Produto'].split('-')[0].strip(), axis=1)
  # print('income', income.info())
  # t = income['Valor da Operação'].str.replace('[^\d.]+', '0', regex=True)
  # idx = income[income['Valor da Operação'].str.contains('-', na=False)].index
  # print(income.loc[idx]['Valor da Operação'].str.replace('-', '0.01'))
  # income.loc[idx]['Valor da Operação'] = income.loc[idx]['Valor da Operação'].str.replace('-', '0.01')
  # idx = income['Valor da Operação'].str.contains('-', na=False)
  # print(idx)
  # print(income.iloc[idx]['Valor da Operação'])
  # income = pd.to_numeric(income['Valor da Operação'], errors = 'coerce')
  # print(income.dtypes, income.shape)
  # income.set_index('Date', inplace=True)
  dataframes.append(income)
  
  # data.append([file_name.date_range, income['Valor líquido'].sum()])
total = pd.concat(dataframes, ignore_index=True)
print('total')
print(total.dtypes, total.shape, total.index)
total.sort_values(by=['Código de Negociação'], inplace=True)
total = income.groupby('Código de Negociação')['Quantidade', 'Valor'].sum()
print(total.shape)
total['median_price'] = total.apply (lambda row: row['Valor']/row['Quantidade'], axis=1)
print(total)
# df = pd.DataFrame(data, columns=['Date', 'Rendimento Mensal'])
# df.set_index('Date', inplace=True)
# df.sort_values(by='Date', inplace=True)
# xlabel = [d.strftime('%b %Y').format()[0] for d in df.index]
# print('date_frame', df, '\n')
# ax = plt.gca()

# ad = df.plot(title="Rendimentos mês a mês", xlabel="Meses", style='.-', color = ['g'], kind='line',y='Rendimento Mensal',ax=ax, rot=90, figsize=(12, 10))

# def my_format_function(x, pos=None):
#     if pos > len(xlabel):
#       return ''
#     return xlabel[pos-1]
# ad.xaxis.set_major_formatter(my_format_function)

# fig,ax1 = plt.subplots()
# plt.plot(df.index,df.values)
# ax1.xaxis.set_major_formatter(monthyearFmt)
# _ = plt.xticks(rotation=90)
# df = pd.DataFrame({'values': np.random.randint(0,1000,36)},index=pd.date_range(start='2014-01-01',end='2016-12-31',freq='M'))
# print(df.dtypes)
# fig,ax1 = plt.subplots()
# plt.plot(df.index,df.values)
# monthyearFmt = mdates.DateFormatter('%Y %B')
# ax1.xaxis.set_major_formatter(monthyearFmt)
# _ = plt.xticks(rotation=90)
# plt.tight_layout()
# plt.savefig("mygraph.png")