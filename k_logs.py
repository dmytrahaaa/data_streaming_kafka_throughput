import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('consumer_timestamps.csv', header=None)
df = df.rename(columns={0:'start_time', 1:'finish_time'})
df['latency'] = df['finish_time'] - df['start_time']

fig, ax = plt.subplots()
ax.plot(df.index, df['latency'])
plt.savefig("latency.png")
plt.show()