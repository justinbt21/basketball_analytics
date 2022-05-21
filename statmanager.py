# -*- coding: utf-8 -*-
"""
Created on Fri May 20 21:43:19 2022

@author: Justin Tran
"""

import json
from nba_api.stats.endpoints import CommonAllPlayers, CommonTeamYears, ShotChartDetail
from nba_api.stats.library.parameters import Season
import pandas as pd

_json = CommonAllPlayers(is_only_current_season=1).get_json()


def _api_scrape(_json_str, index=0):
    _json = json.loads(_json_str)
    
    columns = _json['resultSets'][index]['headers']
    values = _json['resultSets'][index]['rowSet']
    
    return pd.DataFrame(values, columns=columns)

class StatManager(object):
    
    def __init__(self):
        # Initialize player and team list so you will not have to repeat requests to get info
        self.player_list = self._getPlayers()
        self.team_list = self._getTeams()

    def _getPlayers(self, is_current=1, persist=True):
        _json_str = CommonAllPlayers(is_only_current_season=is_current).get_json()
        df = _api_scrape(_json_str)
        
        return df
    
    def _getTeams(self):
        _json_str = CommonTeamYears().get_json()
        df = _api_scrape(_json_str)
        
        return df
    
    def getPlayerID(self, player_name):
        df = self.player_list
        
        id = df[df['DISPLAY_FIRST_LAST'].str.lower() == player_name.lower()]['PERSON_ID']
        id = id.to_string(index=False)
        if len(id) == 0:
            raise Exception('Player could not be found, please try again') 
        
        return id
    
    def getTeamID(self, team_name):
        df = self.team_list
        try:
            id = df[df['ABBREVIATION'].str.lower() == team_name.lower()]['TEAM_ID']
            id = id.to_string(index=False)
        except:
            raise Exception('Team Abbreviation could not be found, please try again')
        
        return id
    
    def getPlayerTeam(self, player_name):
        df = self.player_list
        try:
            id =  df[df['DISPLAY_FIRST_LAST'].str.lower() == player_name.lower()]['TEAM_ID']
            id = id.to_string(index=False)
        except:
            raise Exception('Player could not be found, please try again')
            
        return id
    
    def getPlayerShotChart(self, player_name, year=Season().default):
        player_id = self.getPlayerID(player_name)
        _json = _json = ShotChartDetail(player_id=player_id, team_id=0, season_nullable=year).get_json()
        df = _api_scrape(_json)
        
        return df
    
    
    
    