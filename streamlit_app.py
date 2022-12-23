#importing general objects
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

#TODO: reading in the dataset
median_rent = pd.read_excel('Rent_Data_October2022.xlsx', sheet_name = 0)
median_rent_yoy = pd.read_excel('Rent_Data_October2022.xlsx', sheet_name = 1, header=1)
median_rent_mom = pd.read_excel('Rent_Data_October2022.xlsx', sheet_name = 2, header=1)

pop_data = pd.read_csv('data.csv')
population = pop_data[['pop2022', 'name', 'usps']].copy()
population['name'] = population['name']+ ', ' + population['usps']
population = population.drop('usps', axis=1)
population['name'] = population['name'].str.upper()
population['name'][0] = 'NEW YORK, NY'

area_data = pd.read_csv('uscities.csv')
location = area_data[['city', 'state_id', 'lat', 'lng']].copy()
location['city'] = location['city'].str.upper() + ', ' + location['state_id']
location = location.drop('state_id', axis=1)

median_rent_index = median_rent.set_index('Largest 100 Cities')
dates = median_rent_index.columns.astype(str)
median_rent_T = median_rent_index.transpose()
median_rent_T.insert(0, 'Date', dates)
median_rent_T = median_rent_T.set_index('Date')
median_rent_T = median_rent_T.sort_values(by='2022-10-01 00:00:00', axis=1)
time = (np.linspace(2016, 2022.833, 82))
median_rent_T.insert(0, 'Time', time)

rent_oct_22 = pd.DataFrame(median_rent_T.transpose().iloc[:, -1])
rent_oct_22 = rent_oct_22.drop('Time', axis=0)
rent_pop_2022 = rent_oct_22.merge(population, how='outer', left_on='Largest 100 Cities', right_on='name')
rent_pop_2022 = rent_pop_2022.dropna(axis=0)
rent_pop_2022 = rent_pop_2022.rename(columns={'2022-10-01 00:00:00': 'oct_22_rent'})
rent_pop_2022['oct_22_rent'] = rent_pop_2022['oct_22_rent'].astype(float)
rent_loc = rent_pop_2022.merge(location, how='outer', left_on='name', right_on='city')
rent_loc = rent_loc.dropna(axis=0)
rent_loc = rent_loc.drop('city', axis=1)
rent_loc = rent_loc.rename(columns={'2022-10-01 00:00:00': 'oct_22_rent'})
rent_loc['oct_22_rent'] = rent_loc['oct_22_rent'].astype(float)


#Some basic commands in streamlit -- you can find an amazing cheat sheet here: https://docs.streamlit.io/library/cheatsheet
st.title('Median Rent in Largest US Cities')
st.write('Do rent prices always go up?')
st.markdown("""---""")

#show off a bit of your data. 
st.header('The Data')
col1, col2 = st.columns(2) #here is how you can use columns in streamlit. 
col1.dataframe(median_rent.head())
col2.markdown("\n") #add a line of empty space.
col2.markdown('Here is the original data on the median rent prices in each city, collected once a month from January 2016 to October 2022.') #you can add multiple items to each column.
col2.markdown('As you can see, rent prices vary significantly from city to city, but we may be able to find some general trends in the direction of rent prices.')
st.markdown("""---""")


st.header('Median Rent Price Trends Over Time')
fig = plt.figure(figsize = (20,10))

ax1 = fig.add_subplot(1, 2, 1)
ax1.plot(median_rent_T['Time'], median_rent_T['TOLEDO, OH'], label='Toledo')
ax1.plot(median_rent_T['Time'], median_rent_T['WICHITA, KS'], label='Wichita')
ax1.plot(median_rent_T['Time'], median_rent_T['TULSA, OK'], label='Tolsa')
ax1.plot(median_rent_T['Time'], median_rent_T['LINCOLN, NE'], label='Lincoln')
ax1.plot(median_rent_T['Time'], median_rent_T['OMAHA, NE'], label='Omaha')
ax1.legend()
plt.title('Bottom 5 Median Rent', loc='left')

ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(median_rent_T['Time'], median_rent_T['NEW YORK, NY'], label='New York')
ax2.plot(median_rent_T['Time'], median_rent_T['BOSTON, MA'], label='Boston')
ax2.plot(median_rent_T['Time'], median_rent_T['SAN FRANCISCO, CA'], label='San Francisco')
ax2.plot(median_rent_T['Time'], median_rent_T['JERSEY CITY, NJ'], label='Jersey City')
ax2.plot(median_rent_T['Time'], median_rent_T['IRVINE, CA'], label='Irvine')
ax2.legend()
plt.title('Top 5 Median Rent', loc='left')

st.pyplot(fig)


st.header('Other Data to Add Context')
st.markdown("To get a better idea of factors that might contribute to the median rent price, let's take a look at the population size and location of each city.")
col1, col2 = st.columns(2)
col1.dataframe(population.head())
col2.dataframe(location.head())
st.markdown("""---""")

st.header('Some Plots')
st.plotly_chart(px.histogram(example_data, x="C"))
st.plotly_chart(px.scatter(rent_pop_2022, x="oct_22_rent", y="pop2022", title='Median Rent by Population Size'))
st.plotly_chart(px.scatter(rent_loc, x="lng", y="oct_22_rent", size="pop2022", color="name", title='Median Rent by Longitude and Population'))
st.markdown("This chart plots the longitude, or east/west coordinate, of each city on the x-axis and the median rent price on the y-axis, with the size of the bubble reflecting the population size of the city. Overall, rent prices tend to be higher along the coasts and lower in central US cities, even for central cities with similar population size to coastal cities.")
st.markdown("""---""")

rent_pop_corr = rent_pop_2022[['oct_22_rent', 'pop2022']].corr()

st.dataframe(rent_pop_corr)
st.markdown("There does appear to be a correlation bewteen population size and median rent price, but it appears somewhat weak.")
st.markdown("""---""")

rent_mom = pd.DataFrame(median_rent_mom.median(), columns=['rate of change'])
rent_mom['time'] = time[12:-1]

st.header('Rate of Change')
st.plotly_chart(px.line(rent_mom, x='time', y="rate of change", title='Median Change in Rent Across All Cities Each Month'))
st.markdown("This graph shows the overall median rate of change in rent prices across all cities each month. Although the change in rent price does show prices drop on occasion, the majority of the points are above zero indicating a general trend towards higher rent prices each month.")
st.markdown("""---""")

#Always good to section out your code for readability.
st.header('Conclusions')
st.markdown('- **Data Science is Fun!**')
st.markdown('- **The [Streamlit Cheatsheet](https://docs.streamlit.io/library/cheatsheet) is really useful.**')
