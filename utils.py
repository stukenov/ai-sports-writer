"""
Configuration Utilities
Handles loading of API keys and database configuration from environment files.
"""
import configparser

class OpenAIKeyLoader:
    def __init__(self):
        self.api_key = self.load_openai_api_key()

    def load_openai_api_key(self):
        config = configparser.ConfigParser()
        config.read('.env')
        return config['DEFAULT'].get('OPENAI_API_KEY')

    def get_api_key(self):
        return self.api_key

class MySQLConfigLoader:
    def __init__(self, config_file='.env'):
        self.config_file = config_file
        self.db_config = self.load_mysql_config()

    def load_mysql_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return {
            'user': config['MYSQL'].get('USER'),
            'password': config['MYSQL'].get('PASSWORD'),
            'host': config['MYSQL'].get('HOST'),
            'database': config['MYSQL'].get('DATABASE'),
            'raise_on_warnings': config['MYSQL'].getboolean('RAISE_ON_WARNINGS', fallback=True)
        }

    def get_config(self):
        return self.db_config



if __name__ == "__main__":
    key_loader = OpenAIKeyLoader()
    OPENAI_API_KEY = key_loader.get_api_key()
    if OPENAI_API_KEY:
        print("OPENAI API key loaded successfully.")
        print(f"OPENAI API key: {OPENAI_API_KEY}")
    else:
        print("Failed to load OPENAI API key. Please check the .env file.")
    mysql_config_loader = MySQLConfigLoader()
    db_config = mysql_config_loader.get_config()
    if db_config:
        print("MySQL config loaded successfully.")
    else:
        print("Failed to load MySQL config. Please check the .env file.")