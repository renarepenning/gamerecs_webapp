"""
Adapted from
https://medium.com/@reidtc82/programming-on-hard-mode-4-things-you-need-to-know-about-getting-a-list-of-game-titles-from-igdb-c4337805dedb
This script was used to scrape franchises, game modes, keywords, names, platforms, genres, and all indie games
"""

from operator import itemgetter
import os
import sys
import csv
import time
import json
import requests
# import numpy as np
from igdb.wrapper import IGDBWrapper


LIMIT = 500

# for 500 games from IGDB, fitlered for year and platform
# grab the game id and all franchise ids
def get_games(last, wrap):
	options = 'fields id, franchises; limit 500; offset {0}; where release_dates.y > 2012; where platforms = (6, 165, 163, 130, 162, 167, 14, 48, 169); limit 500;'.format(last)
	time.sleep(.25)

	return wrap.api_request('games', options)


def make_list(end: int=300000):
    last = 0
    # pass in credentials
    client_id = '8kx354hpu7lzs6ga7c1ktafopq30qq'
    client_secret = 'yucgxc2bqiobcn2pfadu5bui5amuan'
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }
    # make the request
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    keys = r.json()
    
    token = keys['access_token']

    # create Access Token
    access_token = token

    # create Wrapper
    wrapper = IGDBWrapper('8kx354hpu7lzs6ga7c1ktafopq30qq', access_token)

    # write to csv
    with open(
        os.path.join(os.getcwd(), 'franchises.csv'),
        'w',
        newline='',
        encoding='utf-8') as myfile:
        wr = csv.writer(myfile)
        for last in range(0, end, LIMIT):
            wr.writerows(
                [item]
                for item in json.loads(
                    get_games(last, wrapper).decode('utf-8').replace("'", '"')
                )
            )


if __name__ == "__main__":
	if len(sys.argv) > 1:
		make_list(int(sys.argv[1]))
	else:
		make_list()