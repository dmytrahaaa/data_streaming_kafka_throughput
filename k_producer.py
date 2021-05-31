from confluent_kafka import Producer
import json
import pandas as pd
import requests

p = Producer({'bootstrap.servers': 'localhost:9091,localhost:9092,localhost:9093'})

subreddit = 'python'
limit = 100 # num of records
timeframe = 'month'  # hour, day, week, month, year, all
listing = 'top'  # controversial, best, hot, new, random, rising, top

def get_reddit(subreddit, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()


def get_post_titles(r):
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        posts.append(x)
    return posts


def get_results(r):
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['title']] = {'url': post['data']['url'], 'score': post['data']['score'],
                                         'comments': post['data']['num_comments'], 'created_date': post['data']['created']}
    df = pd.DataFrame.from_dict(myDict, orient='index')
    return df


r = get_reddit(subreddit, listing, limit, timeframe)
df = get_results(r).reset_index().rename(columns={'index':'title'})
keys = df.columns

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for i in range(df.shape[0]):
    p.poll(0)
    p.produce('my-topic', json.dumps(dict(zip(keys, df.iloc[i].astype('str').values.tolist()))).encode('utf-8'), callback=delivery_report)
    # p.produce('my-topic2', json.dumps(dict(zip(keys, df.iloc[i].astype('str').values.tolist()))).encode('utf-8'), callback=delivery_report)
    # p.produce('my-topic10', json.dumps(dict(zip(keys, df.iloc[i].astype('str').values.tolist()))).encode('utf-8'), callback=delivery_report)

p.flush()
