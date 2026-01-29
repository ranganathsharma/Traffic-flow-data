import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Output.csv')
flow = df['HourlyFlow'].to_numpy()*4
speed = df['meanspeed'].to_numpy()
density = flow/speed

plt.figure(dpi = 400)
plt.scatter(density, flow, marker = '.', s = 1, color = 'r')
plt.xlabel('density (veh/km)', fontsize = 15)
plt.ylabel('flow (veh/hr)', fontsize = 15)
plt.tick_params(axis = 'both', which = 'major', labelsize = 12)
plt.savefig(r'Results\\fundamental_diagram.png', bbox_inches = 'tight')
# plt.show()
plt.close()