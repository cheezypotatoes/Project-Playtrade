import configparser


def create_or_load_ini_file():
    ini_file = 'config.ini'

    config = configparser.ConfigParser()

    if not config.read(ini_file):
        # INI file does not exist, so create it with default values
        config['Settings'] = {
            'Token': 'default_token',
            'ServerID': 'default_server_id'
        }
        with open(ini_file, 'w') as configfile:
            config.write(configfile)
        print(f"INI file '{ini_file}' created with default values.")



