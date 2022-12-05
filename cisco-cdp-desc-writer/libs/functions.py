from os import path, getcwd, system
from netmiko import ConnectHandler

def check_credentials_and_path(username, password, enable_secret, tmp_folder):
    if username == "" or password == "" or enable_secret == "":
        print('username, password or enable_secret cannot be empty. Please enter valid credentials!!!')
        exit()

    if path.isdir(getcwd()+tmp_folder):
        pass    
    else:
        print("The ", tmp_folder, " folder is not exists. Script will create automatically.")
        system('mkdir '+getcwd()+tmp_folder)


def get_cdp_neighbors(ip, username, password, enable_secret, tmp_folder):
    ssh_connection = ConnectHandler(
        device_type = 'cisco_ios',
        ip = ip,
        username = username,
        password = password,
        secret = enable_secret
    )
    ssh_connection.enable()
    result = ssh_connection.find_prompt() + "\n"
    result = ssh_connection.send_command("show cdp neighbors", delay_factor=0)

    with open(getcwd()+tmp_folder+ip, 'w') as outfile:
        outfile.write(result)
    ssh_connection.disconnect()

def write_descr(ip, username, password, enable_secret, localint, descr):
    ssh_connection = ConnectHandler(
        device_type = 'cisco_ios',
        ip = ip,
        username = username,
        password = password,
        secret = enable_secret
    )
    ssh_connection.enable()
    rt = ssh_connection.find_prompt() + "\n"
    rt = ssh_connection.send_command("conf t", delay_factor=0)
    rt = ssh_connection.send_command("int "+localint, delay_factor=0)
    rt = ssh_connection.send_command("description "+descr, delay_factor=0)
    rt = ssh_connection.send_command("do write", delay_factor=0)
    ssh_connection.disconnect()