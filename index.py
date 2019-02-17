from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import pandas as pd
import numpy as np
import json
import zipcodes

TOPIC_NAMES = {"Abortion": "topic:abortion", "Budget + Economy": "topic:budget",
               "Civil Rights": "topic:civil-rights", "Corporations": "topic:corporation",
               "Crime": "topic:crime", "Drugs": "topic:drugs", "Education": "topic:education",
               "Energy + Oil": "topic:energy", "Environment": "topic:environment",
               "Families + Children": "topic:families", "Foreign Policy": "topic:foreign-policy",
               'Free Trade': "topic:free-trade", 'Government Reform': "topic:government-reform",
               'Gun Control': "topic:gun", 'Health Care': "topic:health-care",
               'Homeland Security': "topic:homeland-security", 'Immigration': "topic:immigration",
               'Jobs': "topic:jobs", 'Principles + Values': "topic:principles",
               'Social Security': "topic:social-security", 'Tax Reform': "topic:tax-reform",
               'Technology': "topic:technology", 'War + Peace': "topic:war", 'Welfare + Poverty': "topic:welfare"}

INTENT_NAMES = {"zipcode": "test:zipcode",
                "prompt_topics": "prompt_topics", "election": "election"}

NUM_TOPICS_TO_SELECT = 5

topics_list = []

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    global df
    data = request.get_json(silent=True)
    intent_name = data["queryResult"]["intent"]["displayName"]

    if (intent_name == INTENT_NAMES["zipcode"]):
        zipcode = data['queryResult']['parameters']['zip-code']
        state = zipcodes.matching(zipcode)[0]['state']
        return jsonify({"fulfillmentText": "temp", "followupEventInput":
                        {"name": "zipcode", "parameters": {"state": state}}})

    elif intent_name == INTENT_NAMES["election"]:
        election_type = data["queryResult"]["parameters"]["election"]
        state = data['queryResult']['outputContexts'][0]['parameters']['state']

        if election_type == "House":
            df = pd.read_csv("static/house.csv")
            df.replace(to_replace="_", value=" ", regex=True, inplace=True)
            df = df[df["state"] == state]
            year = "2018"
        elif election_type == "Gubernatorial":
            df = pd.read_csv("static/gov.csv")
            df.replace(to_replace="_", value=" ", regex=True, inplace=True)
            df = df[df["state"] == state]
            year = "2018"
        elif election_type == "Senate":
            df = pd.read_csv("static/senate.csv")
            df.replace(to_replace="_", value=" ", regex=True, inplace=True)
            df = df[df["state"] == state]
            year = "2018"
        elif election_type == "Primary":
            df = pd.read_csv("static/presidential.csv")
            df.replace(to_replace="_", value=" ", regex=True, inplace=True)
            year = "2016"

        num_candidates = len(df["name"].unique())
        num_topics = len(df["topic"].unique())

        select_item = list(np.random.choice(
            df["topic"].unique(), NUM_TOPICS_TO_SELECT))

        return jsonify({"fulfillmentText": "temp", "followupEventInput":
                        {"name": "elec", "parameters": {"num_candidates": str(num_candidates),
                                                        "num_topics": str(num_topics),
                                                        "state": state,
                                                        "election_type": election_type,
                                                        "select_item": select_item,
                                                        "year": year}}})

    elif intent_name == INTENT_NAMES["prompt_topics"]:
        topics = df["topic"].unique()
        topics_to_show = list(np.random.choice(topics, NUM_TOPICS_TO_SELECT))
        topics_string = ", ".join(topics_to_show)
        return_json = {}
        return_json["fulfillmentMessages"] = [
            {
                "text": {
                    "text": [
                        "Here are some topics to choose from: " + topics_string + ". Which ones do you" +
                        " want to choose from? "
                    ]
                }
            }
        ]

        return_json["payload"] = {"messages": [
            {
                "platform": "facebook",
                "replies": [
                    "Quick reply 1",
                    "Quick reply 2",
                    "Quick reply 3"
                ],
                "title": "Quick Reply Title",
                "type": 2
            }
        ]}

        return jsonify(return_json)

    elif intent_name == "candidates":
        df['link'].replace(to_replace=" ", value="_", regex=True, inplace=True)
        bio_series = df.groupby(["name"]).first()

        bio_series.loc[:, "bio"] = bio_series.loc[:, "bio"] + \
            " (" + bio_series.loc[:, "link"] + ")"

        bio_series = bio_series["bio"]

        return_str = ""

        for i in range(len(bio_series)):
            return_str = return_str + bio_series.index.values[i] + "\n\n"
            return_str += bio_series.values[i] + "\n\n"

        print(return_str)

        select_item = list(np.random.choice(
            df["topic"].unique(), NUM_TOPICS_TO_SELECT))

        return jsonify({"fulfillmentText": "temp", "followupEventInput":
                        {"name": "cand", "parameters": {"return_str": return_str, "select_item": select_item}}})

    elif intent_name == "issues":

        list_of_issues = ", ".join(list(df["topic"].unique()))
        select_item = list(np.random.choice(
            df["topic"].unique(), NUM_TOPICS_TO_SELECT))

        return jsonify({"fulfillmentText": "temp", "followupEventInput":
                        {"name": "issu", "parameters": {"list_of_issues": list_of_issues, "select_item": select_item}}})

    for key in TOPIC_NAMES.keys():
        if ((intent_name == (TOPIC_NAMES[key] + " - yes")) or (intent_name == (TOPIC_NAMES[key] + " - no"))):
            select_item = list(np.random.choice(
                df["topic"].unique(), NUM_TOPICS_TO_SELECT))
            return_str = ""
            # return_str = "Feinstein: \n Trump's Supreme Court nominee could end Roe v. Wade. (Jul 2018) \n Partial birth abortion needed for late severe birth defects. (Feb 2015)"
            for candidate in df["name"].unique():
                try:
                    return_str = return_str + candidate + "\n\n"
                    return_str = return_str + df[(df["name"] == candidate)
                                                 & (df["topic"] == key)]["comment"].iloc[0] + "\n\n"
                except:
                    pass

            select_item = list(np.random.choice(
                df["topic"].unique(), NUM_TOPICS_TO_SELECT))

            return jsonify({"fulfillmentText": "temp", "followupEventInput":
                            {"name": "prin", "parameters": {"text": return_str, "select_item": select_item}}})

    return "hello"


# run Flask app
if __name__ == "__main__":
    app.run()
