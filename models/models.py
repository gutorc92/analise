from peewee import *
from abc import ABC, abstractmethod
import logging

# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

db = PostgresqlDatabase('dailyplanet', user='dailyplanet', password='dailyplanet', host='localhost', port=5432)

# db = SqliteDatabase('transaction.db')

class Asset(Model):
    base_ticket = CharField()
    name = CharField()
    real_name = CharField()
    segment = CharField(null=True, choices=(('stock', 'Ações'), ('fi', 'Fundos imobiliários'), ('fii-agro', 'Fundos imobiliários agro')))
    

    class Meta:
        database = db
    
    def __str__(self) -> str:
       return f'{self.base_ticket}'

class Ticket(Model):
    ticket = CharField()
    asset = ForeignKeyField(Asset)
    market = CharField(null=False, choices=(('frac', 'Fracionário'), ('normal', 'Normal')))
    class Meta:
        database = db
    
    def __str__(self) -> str:
       return f'{self.ticket}'

class Cotation(Model):
    ticket = ForeignKeyField(Ticket)
    date = DateField()
    open = DecimalField()
    high = DecimalField()
    low = DecimalField()
    close = DecimalField()
    adj_close = DecimalField()
    volume = DecimalField()

    class Meta:
        database = db

class Transaction(Model):
    ticket = ForeignKeyField(Ticket)
    status = CharField(choices=(('hold', 'Carteira'), ('sell', 'Vendida')))
    date_buy = DateField()
    date_sell = DateField(null=True)
    quantity = IntegerField()
    price = DoubleField()
    total = DoubleField()

    class Meta:
        database = db


    class Meta:
        database = db

class BuyAsset(ABC):
    def __init__(self, ticket, quantity, price, date_buy) -> None:
        self.ticket = ticket
        self.quantity = quantity
        self.price = price
        self.date_buy = date_buy
    
    @abstractmethod
    def execute():
      pass

class BuyStockAsset(BuyAsset):
    
    def __init__(self, ticket, quantity, price, date_buy) -> None:
      super().__init__(ticket, quantity, price, date_buy)
    
    def execute(self):
      is_frac_market = False
      ticket = self.ticket
      if ticket[-1] == 'F':
         is_frac_market = True
         ticket = ticket[:-1]
      asset = Asset.get_or_none(Asset.ticket == ticket)
      print('asset found', is_frac_market, asset)
      if is_frac_market and asset:
        transactions = Transaction.select().where(
          Transaction.asset == asset,
          Transaction.date_buy == self.date_buy
        ).limit(self.quantity)
        if len(transactions) == self.quantity:
          print('len equal')
          return True
        for _ in range(0, self.quantity):
          transaction = Transaction(
              asset=asset,
              status = 'hold',
              date_buy = self.date_buy,
              total=self.price,
              quantity=1, 
              price = self.price
            )
          transaction.save()
class BuyFiAsset(BuyAsset):

    def __init__(self, ticket, quantity, price, date_buy) -> None:
      super().__init__(ticket, quantity, price, date_buy)
    
    def execute(self):
      asset = self.ticket
      if not isinstance(self.ticket, Asset):
        asset = Asset.get(Asset.ticket == self.ticket)
      transactions = Transaction.select().where(
        Transaction.asset == asset,
        Transaction.date_buy == self.date_buy
      ).limit(self.quantity)
      if len(transactions) == self.quantity:
        print('len equal')
        return True
      for _ in range(0, self.quantity):
        transaction = Transaction(
            asset=asset,
            status = 'hold',
            date_buy = self.date_buy,
            total=self.price,
            quantity=1, 
            price = self.price
          )
        transaction.save()

db.create_tables([Asset, Ticket, Transaction, Cotation])