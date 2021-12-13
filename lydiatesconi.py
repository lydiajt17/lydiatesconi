"""
Name:Lydia Tesconi
Date Created: 11/29/2021
Class: Python Section 4
Final Project: Boston Crime
Description:
This python code is meant to interpret Boston crime data with a variety of qualitative and a few
quantitative variables. The variables and information are displayed in interactive elements to fully
show the user interesting patterns in the data set. This information is organized in a table, map, bar chart,
histogram, and pie chart.
"""

# Imported Packages
import folium
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import csv
from streamlit_folium import folium_static

# Listing possible color options to display later
color_box = {'Blue': 'lightblue',
          'Black': 'black',
          'Green': 'lightgreen',
          'Purple': 'magenta',
          'Red': 'red'
          }

# Inserting an crime image to the webpage home page
# https://www.bostonglobe.com/metro/2019/06/01/police-investigate-shooting-roxbury/FgnzhvNocNouqob95r2l4J/story.html
def image():
    from PIL import Image
    img = Image.open("crime.jpg")
    st.image(img, width=700)

# Table of Counts
def table_of_values(df, color_select):
    st.markdown(f"<h1 style='text-align: center; color: {color_select};'>Various Boston Crime Counts</h1>",
                unsafe_allow_html=True)

    # Inserting a select box for the user to choose what count they would like displayed in a table
    option = st.selectbox(
        'What counts would you like to display?',
                               ('Offense_Description', 'Day_of_Week', 'Hour', 'District', 'Shooting', 'Month'))

    # Outputting the value that they select
    st.write('You selected:', option)
    st.write(f"This table displays the number of crimes in each section of "
             f"the {option} category.")

    # Using their option choice, a table of counts for that option is displayed
    if option == "Offense_Description":
        st.write(crimedf.value_counts())
    elif option == "Day_of_Week":
        st.write(daydf.value_counts())
    elif option == "Hour":
        st.write(hourdf.value_counts())
    elif option == "District":
        st.write(districtdf.value_counts())
    elif option == "Shooting":
        st.write(shootingdf.value_counts())
    elif option == "Month":
        st.write(monthdf.value_counts())

def pivot_table(df):
    multi_select = st.selectbox('Choose Columns to Display:',
                               ('Day_of_Week', 'Hour', 'Month', 'District', 'Shooting'))

    table = pd.pivot_table(df, values='MONTH', index='OFFENSE_DESCRIPTION', columns=multi_select.upper(),
                           aggfunc=np.mean, fill_value=0)

    return table


# Creating a map of crimes in various districts
def showonmap(crimelist, color_select):
    st.markdown(f"<h1 style='text-align: center; color: {color_select};'>Map of Crimes in Each District</h1>",
                unsafe_allow_html=True)

    # Sorting districts in ascending order
    district = df['DISTRICT'].sort_values(ascending=True)
    district_list = []

    # Creating a list of districts so that none of the values are repeated
    district_list2 = [district_list.append(x) for x in district if x not in district_list]

    # Select box for a user to select which district's values to analyze
    district_select = st.selectbox("Select a District: ", district_list)

    st.write(f"You have selected {district_select} district! View the map below to "
             f"see the specific locations of the crimes that occurred in that district. ")

    slider = st.slider("Select the Zoom Level: ", 1, 25, 12)

    # Centering the Boston Map for the default
    center = [42.36165764, -71.08567345]
    bostonmap = folium.Map(location=center, zoom_start=slider)

    # Creating popup text for the flag marks to show over each location
    tooltips = "Crime Spot!"

    # Making markers to place over all the lat and lon values in the list of dictionaries referred to in the main func
    for x in crime:
        if x["DISTRICT"] == district_select:
            lat = x.get("Lat")
            lon = x.get("Long")
            folium.Marker(location=
                [lat, lon], popup="flag", icon=folium.Icon(icon="cloud", icon_color=color_select),
                          tooltip=tooltips,
                          ).add_to(bostonmap)
    # Displaying the map
    folium_static(bostonmap)

# Bar plot of days of the week
def bar_chart(daydf, color_select):
    # Counting the number of crimes on each day of the week
    counts = daysdf.value_counts()
    daysdf.dict = counts.to_dict()

    st.write("The purpose of this bar plot is to display the crime frequency of the selected offense "
             "on each day of the week.")

    # Plotting the bar chart
    plt.bar(daysdf.dict.keys(), daysdf.dict.values(), color=color_select)
    plt.xlabel("Days of Week")
    plt.ylabel("Frequency")
    plt.title("Crime Frequency Based on Days of the Week")
    plt.rc('xtick', labelsize=8)
    return plt

# Histogram of crime descriptions
def histogram(df, color_select):
    st.markdown(f"<h1 style='text-align: center; color: {color_select};'>Hour Histogram"
                "</h1>", unsafe_allow_html=True)

    # Select box for the user to interact with
    option = st.selectbox("Select Which Boston Crime You Want to See:", crime_list, index=5)

    # Assigning a new data frame based on the option the user selected
    newdataframe = df[df["OFFENSE_DESCRIPTION"] == option]
    x = newdataframe["HOUR"]

    # Interactive slider for the user to display how many bins they would like to display
    slider = st.slider("Select the Number of Bins to Display", 1, 23, 23)

    st.write(f"This histogram displays the number of {option.lower()} offenses that occur every hour.")

    # Displaying the histogram
    plt.hist(x, density=False, bins=slider, color=color_select)  # density=False would make counts
    plt.ylabel('Frequency')
    plt.xlabel('Hour')
    tick_labels = max(df["HOUR"])
    plt.xticks([x for x in df["HOUR"]])
    plt.title("Frequency of Crimes Committed Each Hour")

    return plt

# Grouping smaller values into an other category in a pie chart and displaying
# https://stackoverflow.com/questions/48587997/matplotlib-pie-graph-with-all-other-categories/48589225
def pie_chart(crimedf):
    counts2 = crimedf.value_counts()
    crimedf_dict = counts2.to_dict()

    df_new = pd.DataFrame(
            data={'offense': crimedf_dict.keys(), 'count': crimedf_dict.values()},
        ).sort_values('count', ascending=False)

    df2 = df_new[:10].copy()

    df_new2 = pd.DataFrame(
    data={'offense': crimedf_dict.keys(), 'count': crimedf_dict.values()},
    ).sort_values('count', ascending=False).head(10)
st.write(df_new)
    new_row = pd.DataFrame(data={
        'offense': ['Others'],
        'count': [df_new['count'][10:].sum()]
    })

    df2 = pd.concat([df2, new_row])

    st.set_option('deprecation.showPyplotGlobalUse', False)

    button = st.button("Click to see a pie chart with all values!!")
    button2 = st.button("Click to see a pie chart with the top 10 values!!")

    if button:
        plt.subplots(figsize=(30, 9))
        plt.pie('count', labels=None, data=df2, autopct="%.2f%%", pctdistance=1.1, radius=1.0, colors=['lightcoral',
                'midnightblue', 'violet', 'deepskyblue', 'chocolate', 'rosybrown', 'slateblue', 'tomato', 'peachpuff',
                                                                                                       'lightcyan', 'royalblue'])
        plt.legend(labels=df2['offense'], loc='upper right', fontsize="x-small")
        plt.title('Top 10 Crimes and Other Category')
        return plt
    if button2:
        plt.subplots(figsize=(30, 9))
        plt.pie('count', labels=None, data=df_new2, autopct="%.2f%%", pctdistance=1.1, radius=1.0, colors=['lightcoral',
                'midnightblue', 'violet', 'deepskyblue', 'chocolate', 'rosybrown', 'slateblue', 'tomato', 'peachpuff',
                                                                                              'royalblue'])
        plt.title('Top 10 Crimes')
        plt.legend(labels=df_new2['offense'], loc='upper right', fontsize="x-small")
        return plt

# Main function
def main():
    # Making certain values global to be used throughout the functions
    global crime
    global crime_list
    global crimedf
    global daydf
    global daysdf
    global hourdf
    global districtdf
    global shootingdf
    global monthdf
    global df
    global areadf
    global color_select

    # Reading in the data file
    FNAME = "crime.csv"
    df = pd.read_csv(FNAME)

    # Reading in a list of dictionaries
    crime = []
    with open(FNAME, 'r') as csv_file:
        crime = list(csv.DictReader(csv_file))
    csv_file.close()
    # Making a list of offenses used in data set
    crime_list = []
    for x in df["OFFENSE_DESCRIPTION"]:
        if x not in crime_list:
            crime_list.append(x)
    crime_list.sort(reverse=True)

    # Creating a variety of data frames to be used throughout the document
    crimedf = df["OFFENSE_DESCRIPTION"]
    daydf = df["DAY_OF_WEEK"]
    hourdf = df["HOUR"]
    districtdf = df["DISTRICT"]
    shootingdf = df["SHOOTING"]
    monthdf = df["MONTH"]
    areadf = df["REPORTING_AREA"]

    # Making an interactive radio sidebar
    side = st.sidebar.radio("Options:", ["Home Page", "About the Data", "District Map", "Offense Bar Chart",
                                         "Time of Day Histogram", "Offense Pie Chart"])
    # Adding an interactive color element
    color_select = st.sidebar.radio("Choose a Color: ", list(color_box.keys()))

    # This changes the page that the user is on to the one that they selected.
    if side == "Home Page":
        st.markdown(f"<h1 style='text-align: center; color: {color_select};'>Boston Crime Analysis</h1>", unsafe_allow_html=True)
        st.write('On this crime webpage you will see a sidebar with different interactive elements to display '
                 'important information about Boston crime. You will see the data displayed in visuals such as a '
                 'table, map, bar chart, histogram, and pie chart. Please view the sidebar to get started!')
        image()
    elif side == "About the Data":
        table_of_values(df, color_select)
        st.write("Pivot Table")
        st.write(pivot_table(df))
    elif side == "District Map":
        showonmap(crime, color_select)
    elif side == "Offense Bar Chart":
        st.markdown(f"<h1 style='text-align: center; color: {color_select};'>Offense Description Bar Plot</h1>",
                unsafe_allow_html=True)
        # Giving the user an opportunity to select which offense to display
        option = st.selectbox("Select Which Boston Crime Offense To Display:", crime_list)
        newdataframe = df[df["OFFENSE_DESCRIPTION"] == option]
        daysdf = newdataframe["DAY_OF_WEEK"]
        st.pyplot(bar_chart(option, color_select), clear_figure=True)
    elif side == "Time of Day Histogram":
        st.pyplot(histogram(df, color_select), clear_figure=True)
    elif side == "Offense Pie Chart":
        st.markdown(f"<h1 style='text-align: center; color: {color_select};'>Pie Chart of Frequent Offenses"
                "</h1>", unsafe_allow_html=True)
        st.pyplot(pie_chart(crimedf))
main()

# References
# https://matplotlib.org/
# https://www.bostonglobe.com/metro/2019/06/01/police-investigate-shooting-roxbury/FgnzhvNocNouqob95r2l4J/story.html
# https://newbedev.com/streamlit-align-text-center-code-example
# https://stackoverflow.com/questions/48587997/matplotlib-pie-graph-with-all-other-categories/48589225
# https://matplotlib.org/stable/gallery/color/named_colors.html
