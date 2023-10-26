#!/usr/bin/env python3

'''
Separates presentation, application processing, and data management functions.
'''

nonlocal objects
objects = {}

from class_Interaction import Interaction
import class_Interaction

def main():
  interaction = Interaction()
  while True:
    interaction.run()

if __name__ == '__main__':
  main()
