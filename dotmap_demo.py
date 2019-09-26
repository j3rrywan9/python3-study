from dotmap import DotMap

credentials = {'username': 'root', 'password': 'sailboat'}

account_info = DotMap(credentials)

print("Username: {}\nPassword: {}".format(account_info.username, account_info.password))

account_info.email = 'john.doe@example.com'

print(account_info.email)
