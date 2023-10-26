#!/usr/bin/env python3

'''
Separates presentation, application processing, and data management functions.
'''

from class_Interaction import Interaction
import class_Interaction

objects = {}

def main():
  global objects
  print(objects)
  interaction = Interaction()
  while True:
    interaction.run()

if __name__ == '__main__':
  main()
