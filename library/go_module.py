#!/usr/bin/python

DOCUMENTATION = '''
---
module: go_module
simple wrapper over go cli
'''
import shutil
import subprocess
import os
from ansible.module_utils.basic import *

def check_and_define_go_binary(go_bin_dir_path):
  go_exec_bin_path = go_bin_dir_path + "/go"  
  result = ''
  if not go_bin_dir_path:
    try:
      shutil.which("go")
      go_exec_bin_path = "go"
    except:  
      print("No installed golang found")
      sys.exit(10)   

  try:
    result=subprocess.run([go_exec_bin_path, "version"], 
                           stdout=subprocess.PIPE)
  except:
    print ("Golang installation broken")
    sys.exit(11) 
  
  return(result.stdout, go_exec_bin_path)

def execute_go_binary_subcommand(go_exec_bin_path, app_path, go_command):
  result = ''
  try:
    os.path.exists(app_path)
  except:
    print("app_path is incorrect")
    sys.exit(12) 
  
  try:
    result=subprocess.run([go_exec_bin_path, go_command],
                           cwd = app_path, 
                           stdout=subprocess.PIPE)
  except:
    print ("Can't run go {} command").format(go_command)  
    sys.exit(13) 

  return(result.stdout)

def check_if_task_state_changed(go_command, command_execution_result):

  is_changed = False

  # if we are building app, consider task as always changed
  if "build" in go_command:
    is_changed = True

  # if command result is non empty - something changed

  if command_execution_result:
    is_changed = True


  return(is_changed)
   

def main():

  argument_spec = {
		"go_bin_path": {"required": False, "type": "str"},
		"app_path": {"required": True, "type": "str" },
    "go_command": {"required": True, "type": "str"}
  }
  module = AnsibleModule(argument_spec=argument_spec)
  
  go_version, go_exec_bin_path=check_and_define_go_binary(module.params["go_bin_path"])

  command_execution_result = execute_go_binary_subcommand(go_exec_bin_path, 
                                                          module.params["app_path"], 
                                                          module.params["go_command"])

  is_changed = check_if_task_state_changed(module.params["go_command"], 
                                           command_execution_result)

  response = {"go_command": module.params["go_command"] , 
              "app_path": module.params["app_path"], 
              "go_version": go_version, 
              "command_result": command_execution_result }
  
  module.exit_json(changed = is_changed, meta = response)


if __name__ == '__main__':
    main()
