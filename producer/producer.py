import pandas as pd
from kafka import KafkaProducer
from kafka.errors import KafkaError
from utils.file_processor import list_files_directory

def on_success(record):
      # print('it pass here', record.offset)
      # print(record.topic)
      # print(record.partition)
      # print(record.offset)
    pass

def on_error(excp):
    log.error(excp)
    raise Exception(excp)

def producer_transactions(directory):
  files_dir = list_files_directory(directory, subdirectory = 'transactions')
  dataframes = []
  for file_name in files_dir:
    income = pd.read_excel(file_name.abs_file_name, decimal=",")
    dataframes.append(income)
    
  total = pd.concat(dataframes, ignore_index=True)
  print('total')
  producer = KafkaProducer(retries=5, bootstrap_servers=['localhost:29092'])
  
  for index, row in total.iterrows():
    producer.send('transction-topic', row.to_json().encode('utf-8')).add_callback(on_success).add_errback(on_error)
  # block until all async messages are sent
  producer.flush()
