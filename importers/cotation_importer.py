import json
import pandas as pd
from datetime import datetime
from models.models import Asset,Ticket, Cotation
import yfinance as yf
import riskfolio as rp


def consume_cotation():
  tickets = Ticket.select().join(Asset).where(Asset.segment == 'fii-agro')
  print(tickets)
  tickets_name = [f'{asset.ticket}' for asset in tickets if asset.ticket[-2:] == '11']
  tickets_query = [f'{asset.ticket}.SA' for asset in tickets if asset.ticket[-2:] == '11']
  print('tickest', tickets_query)
  data = yf.download(tickers = tickets_query,  # list of tickers
              start = '2023-01-01',         # time period
              interval = "1d",       # trading interval
              ignore_tz = True,      # ignore timezone when aligning data from different exchanges?
              prepost = False)
  for ticket in tickets_query:
    ticket_id = [asset for asset in tickets if asset.ticket == ticket[0:-3]][0]
    print(ticket_id)
    data2 = data.loc[:,(['Adj Close', 'Open', 'Volume', 'Close', 'High'], ticket)]
    data2.columns = ['adj_close','open', 'volume', 'close', 'high']
    print('data2', data2.head())
    data2 = data2.dropna()
    print('data2', data2.head())
    for index, row in data2.iterrows():
      converted = row.to_dict()
      try:
        converted['date'] = index
        converted['ticket_id'] = ticket_id.id
        print(converted)
        Cotation.get_or_create(**converted)
      except Exception as e:
        print(e)

  # print(data.columns)
  # df = data[data['Open'] < 10]
  # print(df.index)
  return data, tickets_name

def portifolio(data, assets):
  data2 = data.loc[:,('Adj Close', slice(None))]
  data2.columns = assets
  data3 = data2[data2 < 10.5]
  data4 = data3.dropna(axis=1, how='all')
  Y = data4[assets].pct_change().dropna()
  port = rp.Portfolio(returns=Y)

  # Calculating optimal portfolio

  # Select method and estimate input parameters:

  method_mu='hist' # Method to estimate expected returns based on historical data.
  method_cov='hist' # Method to estimate covariance matrix based on historical data.

  port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

  # Estimate optimal portfolio:

  model='Classic' # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
  rm = 'MV' # Risk measure used, this time will be variance
  obj = 'Sharpe' # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
  hist = True # Use historical scenarios for risk measures that depend on scenarios
  rf = 0 # Risk free rate
  l = 0 # Risk aversion factor, only useful when obj is 'Utility'

  w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
  return w