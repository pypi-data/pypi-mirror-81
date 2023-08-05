
from sqlalchemy import create_engine
import requests
import json

DATABASE = {
    'NAME': 'sandbox',
    'USER': 'read_write_insights',
    'PASSWORD': '5KxPC3bmSTDyo0iXSfZw86R1N657oRdV',
    'HOST': 'mysqldatabase.cmi5f1vp8ktf.us-east-1.rds.amazonaws.com',
    'PORT': '3306',
}

WEBHOOK = 'https://hooks.slack.com/services/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'

def send_webhook(text):
    headers = {'Content-Type': "application/json"}
    slack_data = json.dumps({
        "channel": "#insightful",
        "username": "insightful",
        "icon_emoji": ":thought_balloon:",
        "text": text
    })
    response = requests.post(WEBHOOK, data=slack_data, headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)


def get_mysql_conn(db):
    """
    Return a mysql connection object.
    :params db: a dictionary of database parameters
    """
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{db['USER']}:{db['PASSWORD']}@{db['HOST']}:{db['PORT']}/{db['NAME']}"
        )
        print("MySQL Database Connected...")
        return engine
    except(Exception) as e:
        print('Error while connecting to MySQL...', e)
