import configparser
config = configparser.ConfigParser();

config['DEFAULT'] = {'frameRate': '15',
                     'serverIP': '192.168.1.114',
                     'port': '8080',
                     'playerSpeed' : 8,
                     'RASP' : 0,
                     'winningPoints' : 10}


with open('configFile.ini', 'w') as configfile:
  config.write(configfile)
