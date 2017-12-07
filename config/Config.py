import json


class Config:
    with open('config/config.json') as json_data_file:
        config = json.load(json_data_file)
