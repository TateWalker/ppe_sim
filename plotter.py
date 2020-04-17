import matplotlib.pyplot as plt
import pandas as pd

def plotter(df1,df2):

	fig,ax = plt.subplots()
	df1.plot(kind='line',x='Time',y='GNC Saturation %', ax=ax)
	df1.plot(kind='line',x='Time',y='Distance', ax=ax, secondary_y = True)
	plt.title('GNC Saturation %')
	fig.savefig('export/gncVtime.png',format='png',dpi=100,bbox_inches='tight')

	fig,ax = plt.subplots()
	df1.plot(kind='line',x='Time',y='Data Rate', ax=ax)
	df1.plot(kind='line',x='Time',y='Distance', ax=ax, secondary_y = True)
	plt.title('Data Rate (Mbps)')
	fig.savefig('export/commsVtime.png',format='png',dpi=100,bbox_inches='tight')

	fig,ax = plt.subplots()
	df1.plot(kind='line',x='Time',y='Power Generation Rate', ax=ax)
	df1.plot(kind='line',x='Time',y='Distance', ax=ax, secondary_y = True)
	plt.title('Power Generation Rate (kWh)')
	fig.savefig('export/powerVtime.png',format='png',dpi=100,bbox_inches='tight')

	fig,ax = plt.subplots()
	df2.plot(kind='line',x='Distance',y='Delta V', ax=ax, figsize=(20,1))
	plt.title('Delta V')
	fig.savefig('export/deltavVdistance.png',format='png',dpi=100,bbox_inches='tight')

	