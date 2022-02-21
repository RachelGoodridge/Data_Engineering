# load the required packages
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pickle as pkl
import streamlit as st

st.write("## COVID-19 Cases vs Vaccines in the U.S.")

# retrieve data from pickle
with open("streamlit/dataframe.pkl", "rb") as f:
    df = pkl.load(f)
with open("streamlit/cases2.pkl", "rb") as f:
    cases2 = pkl.load(f)
with open("streamlit/vaccines.pkl", "rb") as f:
    vaccines = pkl.load(f)

# map visualizations
st.write("#### Distribution of COVID cases and vaccines across the United States")
time = st.selectbox("Pick a month and year", df.month.unique(), index=len(df.month.unique())-1)
column = st.selectbox("Pick a topic", ["new cases", "total cases", "deaths", "total deaths", "percent vaccinated", "percent fully vaccinated", "percent boosted"])

if column == "new cases":
    color = "new_cases"
    title = "New COVID Cases" 
    dates = "in {time}".format(time=time)
elif column == "total cases":
    color = "cases"
    title = "Cumulative COVID Cases" 
    dates = "(Jan 2020 - {time})".format(time=time)
elif column == "deaths":
    color = "new_deaths"
    title = "Deaths due to COVID" 
    dates = "in {time}".format(time=time)
elif column == "total deaths":
    color = "deaths"
    title = "Cumulative Deaths due to COVID" 
    dates = "(Jan 2020 - {time})".format(time=time)
elif column == "percent vaccinated":
    color = "perc_vacc"
    title = "Percent of People Vaccinated" 
    dates = "in {time}".format(time=time)
elif column == "percent fully vaccinated":
    color = "perc_full_vacc"
    title = "Percent of People Fully Vaccinated"
    dates = "in {time}".format(time=time)
else:
    color = "perc_boost"
    title = "Percent of People Boosted"
    dates = "in {time}".format(time=time)

if (column == "new cases") or (column == "total cases") or (column == "deaths") or (column == "total deaths"):
    if st.checkbox("per capita", value=True):
        color += "_per_capita"
        title += " Per Capita"
        column += " per capita"
    
fig = px.choropleth(df[df.month == time], locations="abbrev", color=color, hover_data=["state", "pop_size"],
                    locationmode="USA-states", labels={color:column, "pop_size":"population", "abbrev":"abbreviation"})
fig.update_layout(title_text=f"{title} in the United States {dates}", geo_scope="usa", title_x=0.5)
st.plotly_chart(fig)    

st.markdown("""---""")

# dataframe user query of states
st.write("#### Dataframe query to compare between the U.S. states and territories")
column = st.radio("Pick a topic", ["total cases", "cases per capita", "total deaths", "deaths per capita", "percent vaccinated", "percent fully vaccinated", "percent boosted"])
high_low = st.radio("Pick a ranking", ["highest", "lowest"])
dis_num = st.number_input("Display rows", min_value=1, max_value=50, value=5, step=1)

if column == "total cases":
    column = "cases"
    st.write(f"Which {dis_num} states or territories have the {high_low} cumulative number of COVID cases to date?")
elif column == "cases per capita":
    column = "cases_per_capita"
    st.write(f"Which {dis_num} states have the {high_low} cumulative number of COVID cases per capita?")
elif column == "total deaths":
    column = "deaths"
    st.write(f"Which {dis_num} states or territories have the {high_low} cumulative number of deaths from COVID to date?")
elif column == "deaths per capita":
    column = "deaths_per_capita"
    st.write(f"Which {dis_num} states have the {high_low} cumulative number of deaths from COVID per capita?")
elif column == "percent vaccinated":
    column = "perc_vacc"
    st.write(f"Which {dis_num} states or territories have the {high_low} percentage of vaccinated people to date?")
elif column == "percent fully vaccinated":
    column = "perc_full_vacc"
    st.write(f"Which {dis_num} states or territories have the {high_low} percentage of fully vaccinated people to date?")
else:
    column = "perc_boost"
    st.write(f"Which {dis_num} states or territories have the {high_low} percentage of boosted people to date?")

if high_low == "highest":
    st.dataframe(df[df.month == df.month.values[-1]].sort_values(column, ascending=False)[:dis_num][["state", "abbrev", column]])
else:
    st.dataframe(df[df.month == df.month.values[-1]].sort_values(column)[:dis_num][["state", "abbrev", column]])

st.markdown("""---""")

# plot cases, deaths, and vaccines (aggregated by date)
st.write("#### COVID-19 cases over time versus the average percentage of each state vaccinated")
st.write("Configurations for the first graph:")
log = st.checkbox("Plot on a log scale")
count_style = st.radio("Cumulative or Daily?", ["total counts", "new daily counts"])

fig = plt.figure(figsize=(11,4))
ax1 = plt.subplot(1,2,1)
if count_style == "total counts":
    ax1.plot(cases2.index, cases2["cases"], label="Cases")
    ax1.plot(cases2.index, cases2["deaths"], label="Deaths")
    ax1.set_ylabel("Cumulative Counts")
else:
    ax1.plot(cases2.index, cases2["new_cases"], label="Cases")
    ax1.plot(cases2.index, cases2["new_deaths"], label="Deaths")
    ax1.set_ylabel("New Daily Counts")
if log:
    ax1.set_yscale("log")
fig.autofmt_xdate(rotation=45)
ax1.legend()

ax2 = plt.subplot(1,2,2)
ax2.plot(vaccines.date.unique(), vaccines.groupby("date").mean()["perc_vacc"], label="Vaccinated")
ax2.plot(vaccines.date.unique(), vaccines.groupby("date").mean()["perc_full_vacc"], label="Fully Vaccinated")
ax2.plot(vaccines.date.unique(), vaccines.groupby("date").mean()["perc_boost"], label="Boosted")
ax2.set_ylabel("Average Percent Vaccinated")
fig.autofmt_xdate(rotation=45)
ax2.legend()
st.pyplot(fig)

st.markdown("""---""")

st.write("Rachel Goodridge")
st.write("Updated Feb 19, 2022")
st.write("[GitHub](https://github.com/RachelGoodridge/Data_Engineering)")
