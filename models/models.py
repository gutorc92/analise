from peewee import *
from abc import ABC, abstractmethod

db = SqliteDatabase('transaction.db')

class Asset(Model):
    ticket = CharField(unique=True)
    name = CharField()
    real_name = CharField()
    market = CharField(null=True, choices=(('stock', 'Ações'), ('fi', 'Fundos imobiliários'), ('fii-agro', 'Fundos imobiliários agro')))

    class Meta:
        database = db

class Transaction(Model):
    asset = ForeignKeyField(Asset)
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
      
class BuyFiAsset(BuyAsset):

    def __init__(self, ticket, quantity, price, date_buy) -> None:
        super().__init__(ticket, quantity, price, date_buy)
    
    def execute(self):
      asset = Asset.get(Asset.ticket == self.ticket)
      transactions = Transaction.select().where(
        Transaction.asset == asset,
        Transaction.date_buy == self.date_buy
      ).limit(self.quantity)
      if len(transactions) == self.quantity:
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

db.create_tables([Asset, Transaction])