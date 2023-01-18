import os
import json
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import KafkaError
from utils.file_processor import list_files_directory

def on_success(record):
      print('it pass here')
      # print(record.topic)
      # print(record.partition)
      # print(record.offset)

def on_error(excp):
    log.error(excp)
    raise Exception(excp)

def producer_transactions():
  directory = os.path.dirname(os.path.abspath(__file__))
  directory = os.path.join(directory, '..')
  files_dir = list_files_directory(directory, subdirectory = 'transactions')
  dataframes = []
  for file_name in files_dir:
    income = pd.read_excel(file_name.abs_file_name, decimal=",")
    dataframes.append(income)
    
    # data.append([file_name.date_range, income['Valor líquido'].sum()])
  total = pd.concat(dataframes, ignore_index=True)
  print('total')
  producer = KafkaProducer(retries=5, bootstrap_servers=['localhost:29092'])
  # define the on success and on error callback functions
  
  # send the message to fintechexplained-topic
  for index, row in total.iterrows():
    print(index, row.to_json())
    producer.send('transction-topic', row.to_json().encode('utf-8')).add_callback(on_success).add_errback(on_error)
  # block until all async messages are sent
  producer.flush()
