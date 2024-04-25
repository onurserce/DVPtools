import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

df = pd.read_csv('hpc/hpc_benchmark.csv', sep=";")
df = df[-36:]   # Take only the last submitted job

sb.boxplot(data=df, y='ElapsedRaw', x='AllocCPUS')
plt.show()

sb.boxplot(data=df, y='CPUTime', x='ElapsedRaw')
plt.show()

"""
-c=2 gives the best price/performance ratio
with batch_size=10, finishes in about 5 mins
and consumes about 2GB RAM
"""