import connexion
import datetime
import json
import swagger_ui_bundle
import logging
import logging.config
import yaml


def recent_events(body, data=[]):

    with open(STATS_FILE, 'w+') as f:
        for i in f:
            data.append(i)
        data.append(body)

        json.dump(data, f, indent=4)
    logger.info(f"Stored event")

    return data


def buy(body):

    recent_events(body)

    return body, 201


def sell(body):

    recent_events(body)

    return body, 201


def stats():

    with open(STATS_FILE, 'r') as f:
        data = json.load(f)

        buy_event = [i for i in data if 'buy_id' in i]
        sell_event = [i for i in data if 'sell_id' in i]

    result = {}
    max_buy_qty = 0
    max_sell_qty = 0

    for i in buy_event:
        if i["buy_qty"] > max_buy_qty:
            max_buy_qty = i["buy_qty"]

    for i in sell_event:
        if i["sell_qty"] > max_sell_qty:
            max_sell_qty = i["sell_qty"]

    result["max_buy_qty"] = max_buy_qty
    result["max_sell_qty"] = max_sell_qty
    
    logger.info(f"Query Successful")

    return result


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

STATS_FILE = app_config["datastore"]["filename"]

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)