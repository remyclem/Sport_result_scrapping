# coding: utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag

import os
import pandas as pd
import datetime


def reformat_date(current_date_of_match, hour):
    """Convert the scrapped text to a clean datetime object
    
    In particular, handles the first raw which contains "Yesterday"
    instead of the full date
    """
    
    if "Yesterday, " in current_date_of_match:
        year = datetime.datetime.now().year
        current_date_of_match = current_date_of_match.replace("Yesterday, ", "")
        current_date_of_match = current_date_of_match + str(year)
        
    elif "Today, " in current_date_of_match:
        year = datetime.datetime.now().year
        current_date_of_match = current_date_of_match.replace("Today, ", "")
        current_date_of_match = current_date_of_match + str(year)

    full_date_str = current_date_of_match + " " + hour
    full_date_dt = datetime.datetime.strptime(full_date_str, "%d %b %Y %H:%M")
    
    return full_date_dt


def reformat_team_name(team_content):
    """Convert the scrapped text to a clean team name
    
    In particular, removes the " - " between local and visitor
    and removes the "<span>" "markups
    """
    
    if isinstance(team_content, Tag):
        team_content = team_content.contents[0]
    
    team_content = str(team_content).replace(" - ", "")
    
    return team_content


def basket_ball_request(basketball_results_history_csv):

    url_basket_france = "http://www.oddsportal.com/basketball/france/lnb/results/"

    browser = webdriver.Firefox()
    browser.get(url_basket_france)
    html_source = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html_source,'lxml')
    tournament_table = soup.find("table", id="tournamentTable")

    current_date_of_match = ""
    final_table = []

    for row in tournament_table.findAll("tr"):

        # getting the date
        th_elt = row.findAll("th")
        for elt in th_elt:
            span_elt = elt.find("span")
            if span_elt and "datet" in str(span_elt):
                current_date_of_match = span_elt.find(text=True)

        # getting the info per match
        cells = row.findAll("td")

        if len(cells) == 6:
            hour = cells[0].find(text=True)
            date = reformat_date(current_date_of_match, hour)

            match_name_contents = cells[1].find("a").contents
            locals = reformat_team_name(match_name_contents[0])
            visitors = reformat_team_name(match_name_contents[1])
            locals = str(locals)
            visitors = str(visitors)

            score = cells[2].find(text=True)
            score_locals = score.split(":")[0]
            score_visitors = score.split(":")[1]

            odd_locals = cells[3].find(text=True)
            odd_visitors = cells[4].find(text=True)
            nb_bookmakers = cells[5].find(text=True)

            final_table.append(
                [date, locals, visitors, score_locals, score_visitors, odd_locals, odd_visitors, nb_bookmakers])

    columns = ["date", "locals", "visitors", "score_locals", "score_visitors", "odd_locals", "odd_visitors", "nb_bookmakers"]
    basketball_history_df = pd.DataFrame(final_table, columns=columns)
    basketball_history_df.to_csv(basketball_results_history_csv, sep=";", index=False)

