import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
from bss.data.db_path import get_db_path


class Manager:

	def __init__(self, Id, name, password):
		self.Id = Id
		self.name = name
		self.password = password

	def menu_options(self):
		print("Choosing one of the following options.")
		print("1) Growth of company over time")
		print("2) User Behaviour Statistics v1")
		print("3) User Behaviour Statistics v2")
		print("4) Bike Statistics")
		print("5) Daily Usage Frequency Analysis")
		print("6) Response Time from Workers")
		print("7) Quit")
		choice = input()
		while True:
			try:
				choice = int(choice)
				if choice not in range(8):
					raise SystemError
				break
			except:
				print("Invalid choice. Try again!")
		return choice

	def viz(self,choice):

		conn = sqlite3.connect(get_db_path())
		c = conn.cursor()

		if choice == 1:
			transactions = pd.read_sql('Select * from transactions',conn)
			transactions['timeOfEvent'] = [datetime.strptime(i,"%b %d %Y %H:%M:%S").strftime('%b %d %Y') for i in transactions['timeOfEvent']]

			transactions_plot = transactions.groupby(['timeOfEvent']).sum()
			transactions_plot = transactions_plot.cumsum()+1000

			transactions_plot.head()

			plt.figure(figsize=(14,8))
			plt.plot(transactions_plot.index[::len(transactions_plot)//15],transactions_plot[::len(transactions_plot)//15],
			        'r-o',markeredgecolor='k',label='Growth over time')
			plt.grid()
			plt.legend(loc='best')
			plt.title("Growth over time")
			plt.ylabel("Money in company's account")
			plt.xlabel("Dates")
			plt.xticks(transactions_plot.index[::8])
			plt.show()

		if choice == 2:
			transactions = pd.read_sql('Select distance from movement',conn)
			duration = pd.read_sql('Select duration from movement',conn)
			mins = [round((datetime.strptime(i,"%H:%M:%S") - datetime(1900,1,1)).total_seconds()/60,2) for i in duration[duration.columns[0]]]
			charges = pd.read_sql('Select sumOfMoney from transactions',conn)
			charges = charges[charges>0].dropna()

			plt.subplots(1,3,figsize=(20,8))

			plt.subplot(1,3,1)
			plt.boxplot(transactions,notch=True,showmeans=True,meanline=True)
			plt.text(0.8,28,s = str(round(transactions.values.max(),2)))
			plt.text(0.8,12,s = str(round(transactions.values.mean(),2)))
			plt.text(0.8,2,s = str(round(transactions.values.min(),2)))

			plt.ylabel('Distance in Miles')
			plt.title('Distance Travelled')
			plt.xticks([])
			plt.grid('k',linewidth=2)

			plt.subplot(1,3,2)
			plt.boxplot(mins,notch=True,showmeans=True,meanline=True)
			plt.text(0.8,66,s = str(round(pd.DataFrame(mins).values.max(),2)))
			plt.text(0.8,36,s = str(round(pd.DataFrame(mins).values.mean(),2)))
			plt.text(0.8,2,s = str(round(pd.DataFrame(mins).values.min(),2)))

			plt.ylabel('Duration in Minutes')
			plt.title('Duration of Trips')
			plt.xticks([])
			plt.grid('k',linewidth=2)

			plt.subplot(1,3,3)
			plt.boxplot(charges,notch=True,showmeans=True,meanline=True)
			plt.text(0.8,31,s = str(round(charges.values.max(),2)))
			plt.text(0.8,13,s = str(round(charges.values.mean(),2)))
			plt.text(0.8,2,s = str(round(charges.values.min(),2)))

			plt.ylabel('Money')
			plt.title('Cost of Trips')
			plt.xticks([])
			plt.grid('k',linewidth=2)

			plt.show()

		if choice == 3:
			transactions = pd.read_sql('Select distance from movement',conn)
			duration = pd.read_sql('Select duration from movement',conn)
			mins = [round((datetime.strptime(i,"%H:%M:%S") - datetime(1900,1,1)).total_seconds()/60,2) for i in duration[duration.columns[0]]]
			charges = pd.read_sql('Select sumOfMoney from transactions',conn)
			charges = charges[charges>0].dropna()

			plt.subplots(1,3,figsize=(20,8))

			plt.subplot(1,3,1)
			plt.hist(transactions,bins=10,color='b')
			plt.xlabel('Distance in Miles')
			plt.title('Distance Travelled Per Trip')
			plt.ylabel('Number of trips')
			plt.axvline(x=transactions.median()[0],color='r')
			plt.axvline(x=transactions.values.mean(),color='g')

			plt.text(7,110,s = 'Median')
			plt.text(13,100,s = 'Mean')
			plt.grid('k',axis='both',linewidth=2)

			plt.subplot(1,3,2)
			plt.hist(mins,bins=15,color='r')
			plt.axvline(x=transactions.median()[0],color='b',linewidth=2.0)
			plt.axvline(x=transactions.values.mean(),color='g',linewidth=2.0)

			plt.text(3,60,s = 'Median')
			plt.text(13,68,s = 'Mean')

			plt.xlabel('Duration in Minutes')
			plt.ylabel('Number of Trips')
			plt.title('Duration of Trips')
			plt.grid(axis='both',linewidth=1)

			plt.subplot(1,3,3)
			plt.hist(charges,bins=10,color='y')
			plt.xlabel('Money')
			plt.title('Cost Per Trip')
			plt.ylabel('Number of trips')
			plt.axvline(x=charges.median()[0],color='r')
			plt.axvline(x=charges.values.mean(),color='g')

			plt.text(8.5,94,s = 'Median')
			plt.text(14,90,s = 'Mean')
			plt.grid('k',axis='both',linewidth=2)

			plt.show()

		if choice == 4:
			point_of_break = pd.read_sql('Select defective_start from bike_status where defective_start<1',conn)
			point_of_break = point_of_break*100

			fig,ax = plt.subplots(2,1,figsize=(10,8))
			plt.subplot(2,1,1)
			plt.boxplot(point_of_break,notch=True,vert=False,showmeans=True,meanline=True)
			plt.text(94.2,1.2,s = str(round(point_of_break.values.max(),2)))
			plt.text(82,1.2,s = str(round(point_of_break.values.mean(),2)))
			plt.text(32,1.2,s = str(round(point_of_break.values.min(),2)))

			plt.axvline(x=point_of_break.values.min(),color='r')
			plt.axvline(x=point_of_break.values.max(),color='b')
			plt.axvline(x=point_of_break.values.mean(),color='g')
			plt.title("Breaking Point of Bikes")
			plt.yticks([])
			plt.xticks([])

			plt.subplot(2,1,2)
			plt.hist(point_of_break,color='c')
			plt.text(94,72,s = str(point_of_break[point_of_break==point_of_break.max()].count()[0]))
			plt.text(32,1.5,s = str(point_of_break[point_of_break==point_of_break.min()].count()[0]))
			plt.ylabel('Number of Trips')
			plt.xlabel("% Defective")

			plt.show()

		if choice == 5:
			movements = pd.read_sql('Select startTime from movement',conn)

			movements = pd.DataFrame([datetime.strptime(i,"%b %d %Y %H:%M:%S").hour for i in movements['startTime']])
			movements = movements.value_counts().sort_index()
			indexes = [i[0] for i in movements.index.values]
			plt.figure(figsize=(14,7))
			plt.bar(indexes,height=movements.values,color='c')
			plt.plot(indexes,movements.values,color='k',linestyle='--')
			plt.xticks(indexes)
			plt.yticks([10,20,30,40,50])
			plt.grid(axis='both')
			plt.title("Number of Movements vs Time of Day")
			plt.xlabel("Hours of a Day")
			plt.ylabel('No. Of Movements')

			plt.show()

		if choice == 6:
			start_time = pd.read_sql('Select id,time_of_event from bike_status where defective_start<1',conn)
			end_time = pd.read_sql('Select id,time_of_event from bike_status where defective_start=1',conn)	
			start_time['end']=0
			for i in start_time['id'].unique():
			    start_time['end'][start_time['id']==i]=list(end_time['time_of_event'][end_time['id']==i])
			    
			broke_time = [datetime.strptime(i,"%b %d %Y %H:%M:%S") for i in start_time['time_of_event']]
			fixed_time = [datetime.strptime(i,"%b %d %Y %H:%M:%S") for i in start_time['end']]
			response_time = [j-i for i,j in zip(broke_time,fixed_time)]
			response_time = pd.DataFrame([round(divmod(i.seconds,3600)[0] + divmod(i.seconds,3600)[1]/3600) for i in response_time])
			response_time = response_time.value_counts().sort_index()
			indexes =  [i[0] for i in response_time.index.values]
			response_time = list(response_time)
			for i in range(24):
			    if i not in indexes:
			        indexes.append(i)
			        response_time.append(0)

			response_time = pd.DataFrame(response_time,index=indexes)
			response_time = response_time.sort_index()[0].values
			sorted(indexes)
			plt.figure(figsize=(14,7))
			plt.bar(indexes,height=response_time,color='g')
			plt.xticks(indexes)
			plt.yticks([5,10,15,20,25,30,35])
			plt.grid(axis='both')
			plt.title("Response_time")
			plt.xlabel("Hours")
			plt.ylabel('Times')
			plt.show()

		conn.close()
