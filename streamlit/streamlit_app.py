# load the required packages
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pickle as pkl
import streamlit as st

st.write("## COVID-19 Cases vs Vaccines in the U.S.")

# retrieve data from pickle
with open("df.pkl", "rb") as f:
    df = pkl.load(f)
with open("cases2.pkl", "rb") as f:
    cases2 = pkl.load(f)
with open("vaccines.pkl", "rb") as f:
    vaccines = pkl.load(f)

# map visualizations
st.write("Have a look at the distribution of COVID cases and vaccines across the United States.")
time = st.selectbox("Pick a month and year", df.month.unique(), index=len(df.month.unique())-1)
column = st.selectbox("Pick a topic", ["cases", "deaths", "percent vaccinated", "percent fully vaccinated", "percent boosted"])

if column == "cases":
    color = "cases"
    title = "Cumulative COVID Cases"
elif column == "deaths":
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

fig = px.choropleth(df[df.month == time], locations="abbrev", color=color, hover_name="state", locationmode="USA-states")
fig.update_layout(title_text=f"{title} in the United States in {time}", geo_scope="usa", title_x=0.5)
st.plotly_chart(fig)    

st.markdown("""---""")

# dataframe user query of states
st.write("Create your own dataframe query to compare between the U.S. states and territories.")
column = st.radio("Pick a topic", ["cases", "deaths", "percent vaccinated", "percent fully vaccinated", "percent boosted"])
high_low = st.radio("Pick a ranking", ["highest", "lowest"])

if column == "cases":
    st.write(f"Which state or territory has the {high_low} cumulative number of COVID cases to date?")
elif column == "deaths":
    st.write(f"Which state or territory has the {high_low} number of deaths from COVID to date?")
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
st.write("Have a look at the increase in COVID-19 cases over time in comparison to the average percentage of the population that is vaccinated.")
log = st.checkbox("Plot the first graph on a log scale")
if log:
    fig = plt.figure(figsize=(11,4))
    ax1 = plt.subplot(1,2,1) 
    ax1.plot(cases2.index, cases2["cases"], label="Cases")
    ax1.plot(cases2.index, cases2["deaths"], label="Deaths")
    ax1.set_ylabel("Cumulative Counts (log scale)")
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
else:
    fig = plt.figure(figsize=(11,4))
    ax1 = plt.subplot(1,2,1) 
    ax1.plot(cases2.index, cases2["cases"], label="Cases")
    ax1.plot(cases2.index, cases2["deaths"], label="Deaths")
    ax1.set_ylabel("Cumulative Counts")
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
