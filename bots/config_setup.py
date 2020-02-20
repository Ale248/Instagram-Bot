import configparser

config = configparser.ConfigParser()
if config.read('config.ini'):
    print('config found!')
    print('username = ' + config['AUTH']['username'])
    print('password =  ' + config['AUTH']['password'])
    while True:
        choice = input('Change? (y/n) ')
        if choice == 'y':
            new_username = input('New username = ')
            new_password = input('New password = ')

            config['AUTH']['username'] = new_username
            config['AUTH']['password'] = new_password

            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            print('config updated!')
            break
        elif choice == 'n':
            print('config not updated!')
            break
        else:
            print('command not found!')
else:
    print('config not found!')
    print('Setting up a new config...')

    new_username = input('New username = ')
    new_password = input('New password = ')

    config.add_section('AUTH')

    config['AUTH']['username'] = new_username
    config['AUTH']['password'] = new_password

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    print('config created!')

