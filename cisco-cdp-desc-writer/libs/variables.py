from getpass import getpass
input_multiline_string = """
        Write CDP neighbor hostname and portid description to the local interface using SSH...
        Please enter needed credentials

        username: username used for the authentication
        password: password used for the authentication
        enable_secret: enable secret

        """
ip_list_file = 'iplist'
tmp_folder = '/temps/'
allips = open(ip_list_file)
ciscoips = allips.read().splitlines()
allips.close()
print(input_multiline_string)
username = input('Please enter username: ')
password = getpass('Please enter password for '+username+': ')
enable_secret = getpass('Please enter secret: ')