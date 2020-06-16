"""Replace active variables with another set"""
import sys
import os

def replace_env():
  """Replace Variable File"""
  print("Enter Set to Import: ", end='')
  new_env = input()

  if "windows" in sys.platform:
    os.system("copy variable_sets\\" + str(new_env) + ".py user_variables.py")
  else:
    os.system("cp variable_sets/" + str(new_env) + ".py user_variables.py")

replace_env()
