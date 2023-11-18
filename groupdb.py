import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data from the CSV file
file_path = "GroupData2.csv"
data = pd.read_csv(file_path)
# Convert the 'Date' column to datetime format with the correct format
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
# Convert 'Value' column to categorical with specific order
value_order = ['Low', 'Medium', 'High']
data['Value'] = pd.Categorical(data['Value'], categories=value_order, ordered=True)

# Convert 'Value' column to string before grouping
data['Value'] = data['Value'].astype(str)

# Define updated personal hygiene/self-care activities
personal_hygiene_activities_streamlit = [
    'Fix the Bed', 'Brush teeth and Wash Face', 'Morning Routine',
    'Took a Shower', 'Preparing For Church', 'Changed Clothes',
    'Getting Ready for Bed', 'Took a Shower and dressing up for School',
    'Getting Ready for School', 'Got home and dressing up for casual clothes',
    'Prepare to go out to school', 'Wake up and overthink', 'woke Up'
]

# Define leisure, meal, commuting, sleep, and school activities
leisure_activities = [
    'Drove to Mall', 'Wandering in the Mall', 'Went Shopping', 'Using Phone',
    'Workout', 'Chill time', 'Gaming', 'Work on Personal Projects', 'Setup Notion',
    'Play Video Games', 'Watch Anime', 'Wandering around the City', 'Watch Movies', 'Read Manga','Reading'
]
meal_activities = ['Ate Breakfast', 'Ate Lunch', 'Ate Dinner', 'lunch', 'Dinner', 'Lunch', 'Dinner', 'Eating breakfast', 'Breakfast']
commuting_activities = ['Drove to Church', 'Drove to Mall', 'Went Home', 'Commuting', 'commute', 'Commute', 'Went Home/Commuting']
sleep_activities = ['Sleep', 'Sleeping']
school_activities = [
    'Interval of 25mns Study and 5mns Break', 'Doing Activities', 'School', 'Class', 'Academic Tasks',
    'GroupMeetings', 'Do Assigned Task', 'LoungeDuty', 'Morning Class', 'Afternoon Class'
]

# Create a new column 'ActivityGroup' based on the type of activity
data['ActivityGroup'] = data['Activity'].apply(lambda x: 'Personal Hygiene/Self-Care' if x in personal_hygiene_activities_streamlit
                                               else 'Leisure Activities' if x in leisure_activities
                                               else 'Meals' if x in meal_activities
                                               else 'Commuting' if x in commuting_activities
                                               else 'Sleep' if x in sleep_activities
                                               else 'Class/School Work' if x in school_activities
                                               else 'Other Activities')

# Create a new column 'Productivity' based on the type of activity
productive_activities = [
    'Workout', 'Work on Personal Projects', 'Setup Notion', 'Reading Manga',
    'Ate Breakfast', 'Ate Lunch', 'Ate Dinner', 'lunch', 'Dinner', 'Lunch', 'Dinner', 'Eating breakfast', 'Breakfast',
    'Sleep', 'Seeping',
    'Interval of 25mns Study and 5mns Break', 'Doing Activities', 'School', 'Class', 'Academic Tasks',
    'Group Meetings', 'Reading', 'Do Assigned Task', 'Lounge Duty', 'Morning Class', 'Afternoon Class'
]

non_productive_activities = [
    'Drove to Mall', 'Wandering in the Mall', 'Went Shopping', 'Using Phone',
    'Chill time', 'Gaming', 'Play Video Games', 'Watch Anime', 'Wandering around the City',
    'Watch Movies', 'Drove to Church', 'Drove to Mall', 'Went Home', 'Commuting', 'Commute', 'commute',
    'commute', 'Commute', 'Went Home/Commuting'
]

data['Productivity'] = data['Activity'].apply(lambda x: 'Productive' if x in productive_activities
                                                else 'Not Productive' if x in non_productive_activities
                                                else 'Other')


# Calculate the total average of sleep
total_sleep_duration = data[data['ActivityGroup'] == 'Sleep']['Duration(Minutes)'].sum()
total_sleep_entries = data[data['ActivityGroup'] == 'Sleep']['Duration(Minutes)'].count()
average_sleep_duration = total_sleep_duration / total_sleep_entries

# Calculate the total average of leisure
average_leisure_duration = data[data['ActivityGroup'] == 'Leisure Activities']['Duration(Minutes)'].mean()

# Calculate the total average of productive hours spent
total_productive_duration = data[data['Productivity'] == 'Productive']['Duration(Minutes)'].sum()
total_productive_entries = data[data['Productivity'] == 'Productive']['Duration(Minutes)'].count()
average_productive_duration = total_productive_duration / total_productive_entries

# Calculate the percentage of productivity
total_time = data['Duration(Minutes)'].sum()
productivity_percentage = (total_productive_duration / total_time) * 100

# Apply custom CSS
custom_css = """
    .info-box-container {
        display: flex;
        justify-content: space-around;
        
    }
    .info-box {
        flex: 1;
        max-width: calc(25% - 20px);  /* Adjust as needed */
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px;
        text-align: center;
        border-radius: 5px;
        box-shadow: 2px 2px 5px #aaa;
        background-color: #f0f0f0;
    }
"""
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# Display the information in separate boxes using custom CSS
# Create four columns
col1, col2, col3, col4 = st.columns(4)

# Display the information in separate boxes
st.subheader("Dashboard Summary")

# Box for Average Sleep Duration in column 1
with col1:
    st.markdown(f'🛌 <b>Total Average Sleep Duration:</b> {average_sleep_duration:.2f} minutes', unsafe_allow_html=True)

# Box for Average Leisure Time in column 2
with col2:
    st.markdown(f'🎮 <b>Total Average Leisure Time:</b> {average_leisure_duration:.2f} minutes', unsafe_allow_html=True)

# Box for Average Productive Time in column 3
with col3:
    st.markdown(f'🚀 <b>Total Average Productive Time:</b> {average_productive_duration:.2f} minutes', unsafe_allow_html=True)

# Box for Productivity Percentage in column 4
with col4:
    st.markdown(f'💼 <b>Productivity Percentage:</b> {productivity_percentage:.2f}%', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
# Add a button to cycle through different views for the main chart
button_main_chart = st.button("Cycle Through Views (Main Chart)")

# Determine the view based on the button state for the main chart
if button_main_chart:
    current_view_main_chart = st.session_state.get('current_view_main_chart', 'Combined')
    views_main_chart = ['Combined', 'Karl', 'Keath', 'Michael']
    current_index_main_chart = views_main_chart.index(current_view_main_chart)
    next_index_main_chart = (current_index_main_chart + 1) % len(views_main_chart)
    st.session_state['current_view_main_chart'] = views_main_chart[next_index_main_chart]

# Filter data based on the selected view for the main chart
selected_view_main_chart = st.session_state.get('current_view_main_chart', 'Combined')
if selected_view_main_chart == 'Combined':
    filtered_data_main_chart = data
    title_main_chart = 'Combined Distribution of Activities by Total Duration'
else:
    filtered_data_main_chart = data[data['Member'] == selected_view_main_chart]
    title_main_chart = f'Distribution of {selected_view_main_chart}\'s Activities by Total Duration'

# Group the filtered data by activity group and calculate the total duration for each group in Streamlit
activity_group_duration_main_chart = filtered_data_main_chart.groupby('ActivityGroup')['Duration(Minutes)'].sum().reset_index()

# Plotting a treemap in Streamlit for the main chart
fig_main_chart = px.treemap(activity_group_duration_main_chart, path=['ActivityGroup'], values='Duration(Minutes)', title=title_main_chart)

# Calculate the percentage of each slice
percentage_labels_main_chart = (activity_group_duration_main_chart['Duration(Minutes)'] / activity_group_duration_main_chart['Duration(Minutes)'].sum()) * 100

# Add percentage labels and activity names to the treemap chart
fig_main_chart.update_traces(
    hoverinfo='label+percent entry+text',
    text=activity_group_duration_main_chart['ActivityGroup'],
    textinfo='percent entry+text',
    textposition='middle center',
    insidetextfont=dict(size=15),  # You can adjust the font size as needed
    customdata=percentage_labels_main_chart,
)

# Set the size of the chart for the main chart
fig_main_chart.update_layout(width=900, height=800)

# Render the treemap in Streamlit for the main chart
st.plotly_chart(fig_main_chart)


# Add a button to cycle through different views for the productivity chart
button_productivity_chart = st.button("Cycle Through Views (Productivity Chart)")

# Determine the view based on the button state for the productivity chart
if button_productivity_chart:
    current_view_productivity_chart = st.session_state.get('current_view_productivity_chart', 'Combined')
    views_productivity_chart = ['Combined', 'Karl', 'Keath', 'Michael']
    current_index_productivity_chart = views_productivity_chart.index(current_view_productivity_chart)
    next_index_productivity_chart = (current_index_productivity_chart + 1) % len(views_productivity_chart)
    st.session_state['current_view_productivity_chart'] = views_productivity_chart[next_index_productivity_chart]

# Filter data based on the selected view for the productivity chart
selected_view_productivity_chart = st.session_state.get('current_view_productivity_chart', 'Combined')
if selected_view_productivity_chart == 'Combined':
    filtered_data_productivity_chart = data
    title_productivity_chart = 'Combined Distribution of Productive and Non-Productive Activities'
else:
    filtered_data_productivity_chart = data[data['Member'] == selected_view_productivity_chart]
    title_productivity_chart = f'Distribution of Productive and Non-Productive Activities for {selected_view_productivity_chart}'

# Create a new column 'Productivity' based on the type of activity
productive_activities = [
    'Workout', 'Work on Personal Projects', 'Setup Notion', 'Reading Manga',
    'Ate Breakfast', 'Ate Lunch', 'Ate Dinner', 'lunch', 'Dinner', 'Lunch', 'Dinner', 'Eating breakfast', 'Breakfast',
    'Sleep', 'Seeping',
    'Interval of 25mns Study and 5mns Break', 'Doing Activities', 'School', 'Class', 'Academic Tasks',
    'Group Meetings', 'Reading', 'Do Assigned Task', 'Lounge Duty', 'Morning Class', 'Afternoon Class'
]

non_productive_activities = [
    'Drove to Mall', 'Wandering in the Mall', 'Went Shopping', 'Using Phone',
    'Chill time', 'Gaming', 'Play Video Games', 'Watch Anime', 'Wandering around the City',
    'Watch Movies', 'Drove to Church', 'Drove to Mall', 'Went Home', 'Commuting', 'Commute', 'commute',
    'commute', 'Commute', 'Went Home/Commuting'
]

filtered_data_productivity_chart['Productivity'] = filtered_data_productivity_chart['Activity'].apply(lambda x: 'Productive' if x in productive_activities
                                                                                                          else 'Not Productive' if x in non_productive_activities
                                                                                                          else 'Other')

# Create a pie chart to show the distribution of productive and non-productive activities excluding 'Other'
fig_productivity_chart = px.pie(filtered_data_productivity_chart[filtered_data_productivity_chart['Productivity'] != 'Other'],
                                names='Productivity', title=title_productivity_chart)
fig_productivity_chart.update_traces(textinfo='percent+label', pull=[0.1 if 'Other' in filtered_data_productivity_chart['Productivity'].value_counts().index else 0 for _ in filtered_data_productivity_chart['Productivity'].value_counts().index])

# Set the size of the chart for the productivity chart
fig_productivity_chart.update_layout(width=500, height=500)

# Render the pie chart in Streamlit for the productivity chart
st.plotly_chart(fig_productivity_chart)

if 'Class/School Work' in data['ActivityGroup'].unique():
    schoolwork_data_productivity_chart = filtered_data_productivity_chart[
        (filtered_data_productivity_chart['ActivityGroup'] == 'Class/School Work') &
        (filtered_data_productivity_chart['Date'] >= '2023-10-10') &
        (filtered_data_productivity_chart['Date'] <= '2023-10-21')
    ]

    if not schoolwork_data_productivity_chart.empty:
        schoolwork_duration_per_date_productivity_chart = schoolwork_data_productivity_chart.groupby('Date')[
            'Duration(Minutes)'].sum().reset_index()

        fig_schoolwork_chart = px.line(schoolwork_duration_per_date_productivity_chart, x='Date', y='Duration(Minutes)',
                                       title='Week Productivity Trend')
        st.plotly_chart(fig_schoolwork_chart)
    else:
        st.warning("No data available for Schoolwork activities for the specified date range (Oct 10 - Oct 21).")
else:
    st.warning("No data available for Schoolwork activities for the Productivity Chart.")

data['DayOfWeek'] = data['Date'].dt.day_name()
feeling_counts = data.groupby(['DayOfWeek', 'Feeling']).size().reset_index(name='Count')

day_order_mapping = {
    'Sunday': 1,
    'Monday': 2,
    'Tuesday': 3,
    'Wednesday': 4,
    'Thursday': 5,
    'Friday': 6,
    'Saturday': 7
}

feeling_counts['DayOrder'] = feeling_counts['DayOfWeek'].map(day_order_mapping)

feeling_counts = feeling_counts.sort_values(by='DayOrder')

fig_daywise_feeling_trends = px.line(feeling_counts, x='DayOfWeek', y='Count', color='Feeling',
                                     labels={'Count': 'Number of Occurrences', 'DayOfWeek': 'Day of the Week'},
                                     title='Day-wise Feeling Trends')

st.plotly_chart(fig_daywise_feeling_trends)

fig_sentiment_profiles = px.bar(data, x='Member', color='Feeling', title='Individual Sentiment Profiles',
                                category_orders={'Feeling': ['Positive', 'Neutral', 'Negative']},
                                labels={'Feeling': 'Sentiment'})

# Customize the chart layout for the sentiment profiles
fig_sentiment_profiles.update_layout(width=800, height=500, barmode='stack', xaxis_title='Member', yaxis_title='Count')

# Render the chart in Streamlit for sentiment profiles
st.plotly_chart(fig_sentiment_profiles)


# Calculate the average duration of sleep
average_sleep_duration = data[data['ActivityGroup'] == 'Sleep']['Duration(Minutes)'].mean()

# Calculate the productivity percentage for the entire group
total_productive_time = data[data['Productivity'] == 'Productive']['Duration(Minutes)'].sum()
total_non_productive_time = data[data['Productivity'] == 'Not Productive']['Duration(Minutes)'].sum()
total_time = data['Duration(Minutes)'].sum()
productivity_percentage = (total_productive_time / total_time) * 100

# Calculate the average duration of leisure activities
average_leisure_duration = data[data['ActivityGroup'] == 'Leisure Activities']['Duration(Minutes)'].mean()

# Calculate the average duration of productive work
average_productive_duration = data[data['Productivity'] == 'Productive']['Duration(Minutes)'].mean()
