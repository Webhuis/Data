#!/usr/bin/env python3

import class_Ui

def main():
  ui = Ui()

'''
Separates presentation, application processing, and data management functions.
'''

class Data(object):
  ''' Data Store Class '''

  products = {
    'milk': {'price': 1.50, 'quantity': 10},
    'eggs': {'price': 0.20, 'quantity': 100},
    'cheese': {'price': 2.00, 'quantity': 10},
  }

  def __get__(self, obj, klas):
    print('(Fetching from Data Store)')
    return {'products': self.products}

class BusinessLogic(object):
  ''' Business logic holding data store instances '''

  data = Data()

  def product_list(self):
    return self.data['products'].keys()

  def product_information(self, product):
    return self.data['products'].get(product, None)

class Ui(object):
  ''' UI interaction class '''

  def __init__(self):
    self.business_logic = BusinessLogic()

  def get_product_list(self):
    print('PRODUCT LIST:')
    for product in self.business_logic.product_list():
      print(product)
    print('')

  def get_product_information(self, product):
    product_info = self.business_logic.product_information(product)
    if product_info:
      print('PRODUCT INFORMATION:')
      print('Name: {0}, Price: {1:.2f}, Quantity: {2:}'.format(product.title(), product_info.get('price', 0), product_info.get('quantity', 0)))
    else:
      print('That product {0} does not exist in the records'.format(product))

if __name__ == '__main__':
  main()

