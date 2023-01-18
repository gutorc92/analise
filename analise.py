import os
import matplotlib.pyplot as plt
import pandas as pd
from file_processor import FileProcessor

      

def list_files_directory(directory, subdirectory = 'income'):
  files_dir = os.listdir(os.path.join(directory, subdirectory))
  return [FileProcessor(os.path.join(directory, subdirectory, file_name)) for file_name in files_dir]

directory = os.path.dirname(os.path.abspath(__file__))
files_dir = list_files_directory(directory)
data = []
for file_name in files_dir:
  income = pd.read_excel(file_name.abs_file_name, decimal=",")
  data.append([file_name.date_range, income['Valor líquido'].sum()])

df = pd.DataFrame(data, columns=['Date', 'Rendimento Mensal'])
df.set_index('Date', inplace=True)
df.sort_values(by='Date', inplace=True)
xlabel = [d.strftime('%b %Y').format()[0] for d in df.index]
print('date_frame', df, '\n')
ax = plt.gca()

ad = df.plot(title="Rendimentos mês a mês", xlabel="Meses", style='.-', color = ['g'], kind='line',y='Rendimento Mensal',ax=ax, rot=90, figsize=(12, 10))

def my_format_function(x, pos=None):
    if pos > len(xlabel):
      return ''
    return xlabel[pos-1]
ad.xaxis.set_major_formatter(my_format_function)

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
plt.tight_layout()
plt.savefig("mygraph.png")