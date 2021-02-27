# import needed libraries
from twilio.rest import Client
import pandas as pd
import requests
from datetime import datetime
import decouple

# copied from twilio API
account_sid = decouple.config("SID")  # please change it to your own
auth_token = decouple.config("TOKEN")  # please change it to your own
client = Client(account_sid, auth_token)


def send_message(receiver, message):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{receiver}'
    )
    return message


# receiver number
receiver_list = [decouple.config("NUM")]

# get content covid report in Indonesia
url = "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
data_json = requests.get(url).json()

df = []
for row in range(len(data_json["regionData"])):
    df.append(data_json["regionData"][row])
df = pd.DataFrame(df)
data = df.sort_values(['newInfected'], ascending=False)[:3]

# present the data by translating the dataframe to string

region_name = data["region"].tolist()
current_timestamp = str(datetime.now().date())
messages = f"Last Updated on: {current_timestamp}\n" \
           f"Top 3 Indian States sorted by Newly registered cases of COVID-19."
for regions in region_name:
    each_row = data[data["region"] == regions]

    message_partition = f"""
    [{regions}]
    |   Total Infected = {str(each_row['totalInfected'].tolist()[0])}
    |   New Infections =  {str(each_row['newInfected'].tolist()[0])}
    |   Total Recovery = {str(each_row['recovered'].tolist()[0])}
    |   New Recovery = {str(each_row['newRecovered'].tolist()[0])}
    |   Total Deaths = {str(each_row['deceased'].tolist()[0])}
    |   New Deaths = {str(each_row['newDeceased'].tolist()[0])}
    """

    messages = messages + message_partition
