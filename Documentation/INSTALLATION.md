# Installation
*Installation steps required to run the toolkit<br/>
If you see a TODO for something related, please reach out to Aaron Philipose on Slack, Email, or Zoom*

## Windows

### Script Install
- Open Command Line (cmd) and navigate to the Git Directory
- Navigate to setup folder
- Run "powershell.exe -ExecutionPolicy bypass .\install_python.ps1"


### Install indepentantly
- [Download the latest version of Python 3](https://www.python.org/downloads/)
- Run the installer 
  - Use default options.
  - Select to add PYTHON_HOME to PATH
- Open PowerShell or Command Line
  - run "python -m pip install requests"
### Through Company Software Request
- For machines that require Company provided installs, any python version >= 3.4

## Linux

### RHEL, CentOS & Fedora

- Run "sudo yum install python3 python3-pip"
- Run "python3 -m pip install requests"

### Ubuntu & Debian

- Run "sudo apt-get install python3 python3-pip"
- Run "python3 -m pip install requests"