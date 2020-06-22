"""Replace active variables with another set"""
from platform import system
import argparse
import os

def replace_set(set_file):
  """Replace Variable File"""
  # Options are Darwin, Linux, Java and Windows. Java not supported
  if "Windows" in system():
    os.system("copy variable_sets\\" + str(set_file) + ".py user_variables.py")
  else:
    os.system("cp variable_sets/" + str(set_file) + ".py user_variables.py")

def get_variable_set_file(variable_set_arg):
  """Checks if the set file was provided via arg else prompt"""
  if variable_set_arg:
    return variable_set_arg
  return input("Enter Set to Import: ")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--set-file', '-s')
  args = parser.parse_args()
  set_file = get_variable_set_file(args.set_file)
  replace_set(set_file)
