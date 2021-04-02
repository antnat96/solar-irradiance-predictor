import numpy as np
import sys, os
import matplotlib.pyplot as plt
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_yearly
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from IPython.display import display

from geopy.geocoders import Nominatim
import datetime as dt


#place = input ("Enter Address :")
place = "408 brook pine trl, apex, nc"



geolocator = Nominatim(user_agent="Test")
location = geolocator.geocode(place)


years = ['2016','2017','2018','2019']
df = []

lat, lon =  location.latitude, location.longitude
api_key = '5qyFRrBVjEZIGuR0WEcihqCEcg4LV8DbErgE6rze'
attributes = 'ghi'
leap_year = 'false'
interval = '30'
utc = 'false'
your_name = 'Anthony+N'
reason_for_use = 'testing'
your_affiliation = 'ECU'
your_email = 'natalea20@students.ecu.edu'
mailing_list = 'false'

for year in years:
    url = 'https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}'.format(year=year, lat=lat, lon=lon, leap=leap_year, interval=interval, utc=utc, name=your_name, email=your_email, mailing_list=mailing_list, affiliation=your_affiliation, reason=reason_for_use, api=api_key, attr=attributes)
    df.append(pd.read_csv(url, skiprows=2))    

# Concatenate Multiple year data into one DataFrame
big_frame = pd.concat(df, ignore_index=True)
#print(big_frame.shape)


# Set the time index in the pandas dataframe:
#big_frame = big_frame.set_index(pd.date_range('1/1/{yr}'.format(yr=2017), freq=interval+'Min', periods=52560 ))
big_frame = big_frame.set_index(pd.date_range('1/1/{yr}'.format(yr=2016), freq=interval+'Min', periods=70080))


# filtering data 
big_frame=big_frame[(big_frame["GHI"]!=0)]

big_frame.reset_index(inplace=True)


#New DF with just Index & GHI
prophet_frame = big_frame[['index','GHI']]
prophet_frame.head()


# In[122]:


#Renaming columns to ds & y
prophet_frame = prophet_frame.rename(columns = {'index':'ds','GHI':'y'})
prophet_frame['ds']=pd.to_datetime(prophet_frame.ds)


# In[58]:


#prophet_frame.head(5).append(prophet_frame.tail(5))


# In[123]:


prophet_frame = prophet_frame.set_index(['ds'])


# In[124]:


#Group by to get Daily Values
prophet_frame_new = prophet_frame.groupby(prophet_frame.index.date).sum()
prophet_frame_new.reset_index(inplace=True)
prophet_frame_new = prophet_frame_new.rename(columns = {'index':'ds'})
prophet_frame_new['ds']=pd.to_datetime(prophet_frame_new.ds)

#Drop rows with null values
prophet_frame_new.dropna() 


# In[125]:


prophet_frame_new.plot(x='ds',y='y',figsize=(12,8),legend=True,label='GHI Values',xlim=('2016-01-01','2020-01-01'))
#prophet_frame_new.plot.line(x='ds',y='y')


# In[126]:


prophet_frame_new['ds']=pd.to_datetime(prophet_frame_new.ds)
prophet_frame_new.head(5)


# In[94]:


prophet_frame_new.groupby([prophet_frame_new['ds'].dt.year.rename('year')]).agg({'sum'})


# In[107]:


train=prophet_frame_new[:1096]
test=prophet_frame_new[1096:]


#len(prophet_frame_new)
#train.plot()
#train.tail(5)
test.head(5)
#train.plot(x='ds',y='y',figsize=(12,8),legend=True,label='GHI Values')
#train.plot(x='ds',y='y',figsize=(12,8),legend=True,label='GHI Values',xlim=('2016-01-01','2019-12-31'))


# In[129]:


#Model 0
#Initialize Prophet Object
m=Prophet()
#Train the data
m.fit(prophet_frame_new)
#Create Forecasting Time Periods
future=m.make_future_dataframe(periods=365,freq = 'D')
#Forecast using Training data
forecast=m.predict(future)

m.plot(forecast)


plt.xlabel("Date Range")
plt.ylabel("GHI Values")


#forecast.tail()

#ax=forecast.plot(x='ds',y='yhat_upper',legend=True,label='predictions',figsize=(12,8))
#test.plot(x='ds',y='y',legend=True,label='True Test Data',ax=ax,xlim=('2019-01-01','2019-12-31'))


# In[97]:


forecast.head(5).append(forecast.tail(5))


# In[98]:


pd.set_option('display.float_format', '{:.2f}'.format)
dfprint = forecast[["ds",  "yhat"]]
dfprint.groupby([dfprint['ds'].dt.year.rename('year')]).agg({'sum'})


# In[99]:


#Model 1
m1=Prophet(seasonality_mode='multiplicative')
m1.fit(train)

future=m1.make_future_dataframe(periods=365,freq = 'D') 
forecast=m1.predict(future)
#forecast.tail()


ax=forecast.plot(x='ds',y='yhat',legend=True,label='predictions',figsize=(12,8))
test.plot(x='ds',y='y',legend=True,label='True Test Data',ax=ax,xlim=('2019-01-01','2019-12-31'))


# In[100]:


dfprint = forecast[["ds", "trend","yhat_lower", "yhat_upper", "yhat"]]
dfprint.head(5).append(dfprint.tail(5))
pd.set_option('display.float_format', '{:.2f}'.format)
dfprint = forecast[["ds",  "yhat"]]
dfprint.groupby([dfprint['ds'].dt.year.rename('year')]).agg({'sum'})


# In[101]:


#Model 2
#m2 = Prophet(seasonality_mode='multiplicative',daily_seasonality=True,interval_width=0.95,changepoint_prior_scale=2)
m2 = Prophet(interval_width=0.85,changepoint_prior_scale=5,yearly_seasonality=True,daily_seasonality=True)
m2.fit(train)

future=m2.make_future_dataframe(periods=365,freq = 'D') 
forecast=m2.predict(future)


ax=forecast.plot(x='ds',y='yhat',legend=True,label='predictions',figsize=(12,8))
test.plot(x='ds',y='y',legend=True,label='True Test Data',ax=ax,xlim=('2019-01-01','2019-12-31'))


# In[102]:


dfprint = forecast[["ds", "trend","yhat_lower", "yhat_upper", "yhat"]]
dfprint.head(5).append(dfprint.tail(5))
pd.set_option('display.float_format', '{:.2f}'.format)
dfprint = forecast[["ds",  "yhat"]]
dfprint.groupby([dfprint['ds'].dt.year.rename('year')]).agg({'sum'})


# In[103]:


#Model 3
m3 = Prophet(interval_width=0.85,changepoint_prior_scale=5,daily_seasonality=True,yearly_seasonality=20)
m3.add_seasonality(name='daily', period=365.25, fourier_order=5, prior_scale=0.02)
m3.fit(train)

future=m3.make_future_dataframe(periods=365,freq = 'D') 
forecast=m3.predict(future)


ax=forecast.plot(x='ds',y='yhat',legend=True,label='predictions',figsize=(12,8))
test.plot(x='ds',y='y',legend=True,label='True Test Data',ax=ax,xlim=('2019-01-01','2019-12-31'))


# In[104]:


dfprint = forecast[["ds", "trend","yhat_lower", "yhat_upper", "yhat"]]
dfprint.head(5).append(dfprint.tail(5))
pd.set_option('display.float_format', '{:.2f}'.format)
dfprint = forecast[["ds",  "yhat"]]
dfprint.groupby([dfprint['ds'].dt.year.rename('year')]).agg({'sum'})


# In[105]:


m4 = Prophet(interval_width=0.95,changepoint_prior_scale=7,daily_seasonality=True)
m4.add_seasonality(name='monthly', period=12, fourier_order=5)

m4.fit(train)

future=m4.make_future_dataframe(periods=365,freq = 'D') 
#future=m4.make_future_dataframe(periods=12,freq='MS') 
forecast=m4.predict(future)


ax=forecast.plot(x='ds',y='yhat',legend=True,label='predictions',figsize=(12,8))
test.plot(x='ds',y='y',legend=True,label='True Test Data',ax=ax,xlim=('2019-01-01','2019-12-31'))


# In[106]:


dfprint = forecast[["ds", "trend","yhat_lower", "yhat_upper", "yhat"]]
dfprint.head(5).append(dfprint.tail(5))
pd.set_option('display.float_format', '{:.2f}'.format)
dfprint = forecast[["ds",  "yhat"]]
dfprint.groupby([dfprint['ds'].dt.year.rename('year')]).agg({'sum'})


# In[134]:


#Picking Model 3 and forecasting for next 2 years
#Model 3
m3 = Prophet(interval_width=0.85,changepoint_prior_scale=5,daily_seasonality=True,yearly_seasonality=20)
m3.add_seasonality(name='daily', period=365.25, fourier_order=5, prior_scale=0.02)
m3.fit(prophet_frame_new)

future3=m3.make_future_dataframe(periods=730,freq = 'D') 
forecast3=m3.predict(future3)


m3.plot(forecast3)


plt.xlabel("Date Range")
plt.ylabel("GHI Values")



# In[135]:


dfprint3 = forecast3[["ds", "trend","yhat_lower", "yhat_upper", "yhat"]]
#dfprint.head(5).append(dfprint.tail(5))
pd.set_option('display.float_format', '{:.2f}'.format)
dfprint3 = forecast3[["ds",  "yhat"]]
dfprint3.groupby([dfprint3['ds'].dt.year.rename('year')]).agg({'sum'})

#ax=forecast.plot(x='ds',y='yhat',legend=True,label='predictions',figsize=(12,8))
#test.plot(x='ds',y='y',legend=True,label='True Test Data',ax=ax,xlim=('2019-01-01','2019-12-31'))

"""