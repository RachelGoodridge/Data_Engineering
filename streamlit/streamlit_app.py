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
with open("streamlit/cases.pkl", "rb") as f:
    temp = pkl.load(f)
with open("streamlit/counties.pkl", "rb") as f:
    counties = pkl.load(f)

# map visualizations
st.write("#### Distribution of COVID cases and vaccines across the United States")
time = st.selectbox("Pick a month and year", df.month.unique(), index=len(df.month.unique())-1)
column = st.selectbox("Pick a topic", ["new cases", "total cases", "new deaths", "total deaths", "percent vaccinated", "percent fully vaccinated", "percent boosted"])

if column == "new cases":
    color = "new_cases"
    title = "New COVID Cases"
elif column == "total cases":
    color = "cases"
    title = "Cumulative COVID Cases"
elif column == "new deaths":
    color = "new_deaths"
    title = "New Deaths due to COVID"
elif column == "total deaths":
    color = "deaths"
    title = "Cumulative Deaths due to COVID"
elif column == "percent vaccinated":
    color = "perc_vacc"
    title = "Percent of People Vaccinated"
elif column == "percent fully vaccinated":
    color = "perc_full_vacc"
    title = "Percent of People Fully Vaccinated"
else:
    color = "perc_boost"
    title = "Percent of People Boosted"

if (column == "new cases") or (column == "total cases") or (column == "new deaths") or (column == "total deaths"):
    if st.checkbox("per capita", value=True):
        color += "_per_capita"
        title += " Per Capita"
    
fig = px.choropleth(df[df.month == time], locations="abbrev", color=color, hover_data=["state", "pop_size"],
                    locationmode="USA-states", labels={color:column, "pop_size":"population", "abbrev":"abbreviation"})
fig.update_layout(title_text=f"{title} in the United States in {time}", geo_scope="usa", title_x=0.5)
st.plotly_chart(fig)    

st.markdown("""---""")

# dataframe user query of states
st.write("#### Dataframe query to compare between the U.S. states and territories")
column = st.radio("Pick a topic", ["total cases", "cases per capita", "total deaths", "deaths per capita", "percent vaccinated", "percent fully vaccinated", "percent boosted"])
high_low = st.radio("Pick a ranking", ["highest", "lowest"])

if column == "total cases":
    column = "cases"
    st.write(f"Which state or territory has the {high_low} cumulative number of COVID cases to date?")
elif column == "cases per capita":
    column = "cases_per_capita"
    st.write(f"Which state has the {high_low} cumulative number of COVID cases per capita?")
elif column == "total deaths":
    column = "deaths"
    st.write(f"Which state or territory has the {high_low} cumulative number of deaths from COVID to date?")
elif column == "deaths per capita":
    column = "deaths_per_capita"
    st.write(f"Which state or territory has the {high_low} cumulative number of deaths from COVID per capita?")
elif column == "percent vaccinated":
    column = "perc_vacc"
    st.write(f"Which state or territory has the {high_low} percentage of vaccinated people to date?")
elif column == "percent fully vaccinated":
    column = "perc_full_vacc"
    st.write(f"Which state or territory has the {high_low} percentage of fully vaccinated people to date?")
else:
    column = "perc_boost"
    st.write(f"Which state or territory has the {high_low} percentage of boosted people to date?")

if high_low == "highest":
    mask = df[df.month == df.month.values[-1]][column] == max(df[df.month == df.month.values[-1]][column])
else:
    mask = df[df.month == df.month.values[-1]][column] == min(df[df.month == df.month.values[-1]][column])
    
st.dataframe(df[df.month == df.month.values[-1]][mask][["state", "abbrev", "month", column]])

st.markdown("""---""")

# plot cases, deaths, and vaccines (aggregated by date)
st.write("#### COVID-19 cases versus the average percentage vaccinated over time")
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

# map visualizations by county
st.write("#### Distribution of COVID cases grouped by county")
topic = st.radio("Pick a topic", ["cases", "deaths"])

if topic == "cases":
    title = "Cumulative COVID Cases in the United States by County"
else:
    title = "Cumulative Deaths due to COVID in the United States by County"

fig = px.choropleth(temp, geojson=counties, locations="fips", color=topic, hover_data=["state", "county"])
fig.update_layout(title_text=title, geo_scope="usa", title_x=0.5)
st.plotly_chart(fig) 