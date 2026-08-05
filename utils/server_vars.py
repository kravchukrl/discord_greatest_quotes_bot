import os
import json
cog_folder = os.path.dirname(__file__)
dirname = os.path.split(cog_folder)[0]
configs_json = os.path.join(dirname, "utils/server_configs.json")
with open(configs_json, "r") as configs:
    server_configs = json.load(configs)
    server_to_quotes = {}
    server_to_threshold = {}
    server_to_restricted = {}
    for server in server_configs:
        server_pair = server_configs[server]
        id = server_pair["server_id"]
        server_to_quotes[id] = server_pair["quotes_id"]
        server_to_threshold[id] = server_pair["threshold"]
        server_to_restricted[id] = server_pair["restricted"].values()