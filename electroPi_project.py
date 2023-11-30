import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Replace these values with your MySQL server details


def plot_users(data, x_col, y_col, mode, name, line_color=None, bar_opacity=None):
    trace = go.Scatter(
        x=data[x_col].astype(str),  # Convert the date column to string for plotting
        y=data[y_col],
        mode=mode,
        name=name,
        line=dict(color=line_color),
        opacity=bar_opacity
    )
    return trace


db_config = {
   "host": "localhost",
   "user": "root",
   "password": "mena Fci 4321",
   "database": "electro_pi_database",
}

connection = mysql.connector.connect(**db_config)

cursor = connection.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM users")

# Fetch and print the results


# st.header('Package of users')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
users = pd.DataFrame(result, columns=column_names)
# st.write(users)
#1
st.header(1)
#--------------------------------------------

users['registration_date'] = pd.to_datetime(users['registration_date'])
users['registration_date'] = pd.to_datetime(users['registration_date'])

# Create additional columns for different time periods
users['Day'] = users['registration_date'].dt.date
users['Week'] = users['registration_date'].dt.strftime('%Y-%U')
users['Month'] = users['registration_date'].dt.strftime('%Y-%m')
users['Year'] = users['registration_date'].dt.year

# Group the data by the desired time period and count the number of registered and subscribed users

daily_users = users.groupby(['Day', 'subscribed']).size().unstack(fill_value=0).reset_index()
weekly_users = users.groupby(['Week', 'subscribed']).size().unstack(fill_value=0).reset_index()
monthly_users = users.groupby(['Month', 'subscribed']).size().unstack(fill_value=0).reset_index()
yearly_users = users.groupby(['Year', 'subscribed']).size().unstack(fill_value=0).reset_index()

# Filter for daily registered users
daily_registered_users = daily_users[['Day', 0]].rename(columns={0: 'Daily Registered Users'})

# Filter for weekly registered users
weekly_registered_users = weekly_users[['Week', 0]].rename(columns={0: 'Weekly Registered Users'})

# Filter for monthly registered users
monthly_registered_users = monthly_users[['Month', 0]].rename(columns={0: 'Monthly Registered Users'})

# Filter for yearly registered users
yearly_registered_users = yearly_users[['Year', 0]].rename(columns={0: 'Yearly Registered Users'})

# Filter for daily subscribed users
daily_subscribed_users = daily_users[['Day', 1, 2]].rename(columns={1: 'Daily Subscribed Users', 2: 'Daily Paid Subscribers'})

# Filter for weekly subscribed users
weekly_subscribed_users = weekly_users[['Week', 1, 2]].rename(columns={1: 'Weekly Subscribed Users', 2: 'Weekly Paid Subscribers'})

# Filter for monthly subscribed users
monthly_subscribed_users = monthly_users[['Month', 1, 2]].rename(columns={1: 'Monthly Subscribed Users', 2: 'Monthly Paid Subscribers'})

# Filter for yearly subscribed users
yearly_subscribed_users = yearly_users[['Year', 1, 2]].rename(columns={1: 'Yearly Subscribed Users', 2: 'Yearly Paid Subscribers'})

# Create the figure and add traces
# fig = go.Figure()

# # Add traces for registered users
# fig.add_trace(go.Scatter(x=daily_users['Day'], y=daily_users['Registered Users'], name='Daily Registered Users'))
# fig.add_trace(go.Scatter(x=weekly_users['Week'], y=weekly_users['Registered Users'], name='Weekly Registered Users'))
# fig.add_trace(go.Scatter(x=monthly_users['Month'], y=monthly_users['Registered Users'], name='Monthly Registered Users'))
# fig.add_trace(go.Bar(x=yearly_users['Year'], y=yearly_users['Registered Users'], name='Yearly Registered Users'))

# # Add trace for subscribed users
# fig.add_trace(go.Scatter(x=subscribed_users['Day'], y=subscribed_users['Subscribed Users'], name='Daily Subscribed Users'))

# # Set layout properties
# fig.update_layout(title='Registered and Subscribed Users',
#                   xaxis_title='Time Period',
#                   yaxis_title='Number of Users')

# # Display the graph in Streamlit
# st.plotly_chart(fig, use_container_width=True)





# Create a multiselect dropdown for user selection
selected_metrics = st.multiselect(
    'Select metrics to visualize',
    ['Daily registered user', 'Weekly registered user', 'Monthly registered user', 'Yearly registered user',
     'Daily subscribed user', 'Weekly subscribed user', 'Monthly subscribed user', 'Yearly subscribed user'],
    default=['Daily registered user', 'Daily subscribed user']
)

# Define a mapping for the selected metrics
metric_mapping = {
    'Daily registered user': (daily_registered_users, 'Day', 'Daily Registered Users', 'lines+markers', 'Daily Registered Users', 'blue', None),
    'Weekly registered user': (weekly_registered_users, 'Week', 'Weekly Registered Users', 'lines+markers', 'Weekly Registered Users', 'orange', None),
    'Monthly registered user': (monthly_registered_users, 'Month', 'Monthly Registered Users', 'lines+markers', 'Monthly Registered Users', 'green', None),
    'Yearly registered user': (yearly_registered_users, 'Year', 'Yearly Registered Users', 'lines', 'Yearly Registered Users', 'red', 0.5),
    'Daily subscribed user': (daily_subscribed_users, 'Day', 'Daily Subscribed Users', 'lines+markers', 'Daily Subscribed Users', 'purple', None),
    'Weekly subscribed user': (weekly_subscribed_users, 'Week', 'Weekly Subscribed Users', 'lines+markers', 'Weekly Subscribed Users', 'brown', None),
    'Monthly subscribed user': (monthly_subscribed_users, 'Month', 'Monthly Subscribed Users', 'lines+markers', 'Monthly Subscribed Users', 'pink', None),
    'Yearly subscribed user': (yearly_subscribed_users, 'Year', 'Yearly Subscribed Users', 'lines', 'Yearly Subscribed Users', 'gray', 0.5)
}

# Create the figure and add traces based on user selection
fig = go.Figure()

for metric in selected_metrics:
    data, x_col, y_col, mode, name, line_color, bar_opacity = metric_mapping[metric]
    fig.add_trace(plot_users(data, x_col, y_col, mode, name, line_color, bar_opacity))

# Set layout properties
fig.update_layout(
    title='User Metrics Over Time',
    xaxis_title='Time Period',
    yaxis_title='Number of Users',
    legend=dict(x=0, y=1, traceorder='normal', orientation='h'),
    barmode='overlay'  # Overlay bars for yearly data
)

# Display the graph in Streamlit
st.plotly_chart(fig, use_container_width=True)










#2
st.header(2)
#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM bundles")



# st.header('Package of bundles')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]
# Create a DataFrame
bundles = pd.DataFrame(result, columns=column_names)

# Convert the date columns to datetime format
bundles['creation_date'] = pd.to_datetime(bundles['creation_date'])

# Create additional columns for different time periods
bundles['Day'] = bundles['creation_date'].dt.date
bundles['Week'] = bundles['creation_date'].dt.strftime('%Y-%U')
bundles['Month'] = bundles['creation_date'].dt.strftime('%Y-%m')
bundles['Year'] = bundles['creation_date'].dt.year

# Group the data by the desired time period and count the number of subscribed users for each bundle
daily_subscriptions = bundles.groupby(['Day', 'bundle_name']).size().reset_index(name='Subscribed Users')
weekly_subscriptions = bundles.groupby(['Week', 'bundle_name']).size().reset_index(name='Subscribed Users')
monthly_subscriptions = bundles.groupby(['Month', 'bundle_name']).size().reset_index(name='Subscribed Users')
yearly_subscriptions = bundles.groupby(['Year', 'bundle_name']).size().reset_index(name='Subscribed Users')

# Create the figure and add traces
fig = go.Figure()

# Add traces for daily subscriptions
for bundle in bundles['bundle_name'].unique():
    fig.add_trace(go.Bar(x=daily_subscriptions[daily_subscriptions['bundle_name'] == bundle]['Day'],
                         y=daily_subscriptions[daily_subscriptions['bundle_name'] == bundle]['Subscribed Users'],
                         name=f'Daily Subscriptions - {bundle}'))

# Add traces for weekly subscriptions
for bundle in bundles['bundle_name'].unique():
    fig.add_trace(go.Bar(x=weekly_subscriptions[weekly_subscriptions['bundle_name'] == bundle]['Week'],
                         y=weekly_subscriptions[weekly_subscriptions['bundle_name'] == bundle]['Subscribed Users'],
                         name=f'Weekly Subscriptions - {bundle}'))

# Add traces for monthly subscriptions
for bundle in bundles['bundle_name'].unique():
    fig.add_trace(go.Bar(x=monthly_subscriptions[monthly_subscriptions['bundle_name'] == bundle]['Month'],
                         y=monthly_subscriptions[monthly_subscriptions['bundle_name'] == bundle]['Subscribed Users'],
                         name=f'Monthly Subscriptions - {bundle}'))

# Add traces for yearly subscriptions
for bundle in bundles['bundle_name'].unique():
    fig.add_trace(go.Bar(x=yearly_subscriptions[yearly_subscriptions['bundle_name'] == bundle]['Year'],
                         y=yearly_subscriptions[yearly_subscriptions['bundle_name'] == bundle]['Subscribed Users'],
                         name=f'Yearly Subscriptions - {bundle}'))

# Set layout properties
fig.update_layout(title='Subscribed Users by Bundle',
                  xaxis_title='Time Period',
                  yaxis_title='Number of Subscribed Users')

# Display the graph in Streamlit
st.plotly_chart(fig, use_container_width=True)




# #----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM user_completed_courses")

# Fetch and print the results


# st.header('Package of user_completed_courses')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
user_completed_courses = pd.DataFrame(result, columns=column_names)
# st.write(user_completed_courses)


# #----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM courses")

# Fetch and print the results


# st.header('Package of courses')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
courses = pd.DataFrame(result, columns=column_names)
# st.write(courses)









#3
st.header(3)
# Prompt the user to enter a user ID
user_id = st.text_input("Enter the User ID:")
users_10k = users[users['10k_AI_initiative'] == 1]
# Check if the input is a valid number
if user_id.isdigit():
    user_id = int(user_id)

    # Check if the user is in the 10k AI Initiative
    if user_id in users_10k['user_id'].tolist():
        # Filter completion data for the specified user ID
        user_completion_data = user_completed_courses[user_completed_courses['user_id'] == user_id]

        # Merge completion data with course data
        completion_course_df = user_completion_data.merge(courses, on='course_id')

        # Get the last completed course information for the user
        last_completed_course = completion_course_df.iloc[-1]
        
        # Group completion data by user and count the number of completed courses
        completed_courses = completion_course_df.groupby('user_id').size().reset_index(name='Completed Courses')

        # Merge completed courses data with users data
        users_completed_df = users_10k.merge(completed_courses, on='user_id', how='left')

        # Merge users completed data with the last completed course information
        users_last_completed = users_completed_df.merge(completion_course_df.groupby('user_id').last().reset_index(), on='user_id')

        # Sort users by 'course_degree' and 'Completed Courses'
        sorted_users_10k = users_last_completed.sort_values(by=['course_degree', 'Completed Courses'], ascending=[False, False])

        columns_to_display = ['user_id', 'Completed Courses', 'course_degree', 'completion_date']
        st.write(sorted_users_10k[columns_to_display])

       

    else:
        st.write(f"User {user_id} is not in the 10k AI Initiative.")
else:
    st.write("Invalid input. Please enter a valid User ID.")


# Merge completion data with course data
completion_course_df = user_completed_courses.merge(courses, on='course_id')

# Group completion data by user and count the number of completed courses
completed_courses = completion_course_df.groupby('user_id').size().reset_index(name='Completed Courses')

# Merge completed courses data with users data
users_completed_df = users_10k.merge(completed_courses, on='user_id', how='left')

# Merge users completed data with the last completed course information
users_last_completed = users_completed_df.merge(completion_course_df.groupby('user_id').last().reset_index(), on='user_id')

# Sort users by 'course_degree' and 'Completed Courses'
sorted_users_10k = users_last_completed.sort_values(by=['course_degree', 'Completed Courses'], ascending=[False, False])

# Display the sorted table
st.header("this is sorted 10k_AI_initiative")
st.write(sorted_users_10k)

# Create a scatter plot to show the number of completed courses for each user
fig_all_users_scatter = go.Figure(data=[
    go.Scatter(x=sorted_users_10k['user_id'],
               y=sorted_users_10k['Completed Courses'],
               mode='markers+text',
               marker=dict(
                   symbol='diamond',  # You can try different symbols (e.g., 'circle', 'square', 'diamond')
                   size=10,
                   color='rgb(158,202,225)',
                   line=dict(color='rgb(8,48,107)', width=1)  # Marker border color and width
               ),
               text=sorted_users_10k['Completed Courses'],
               textposition='bottom center',
               hovertemplate='<b>User ID: %{x}</b><br>' +
                             'Completed Courses: %{y}<br>'
               )
])

# Set layout properties for the all users scatter plot
fig_all_users_scatter.update_layout(
    title="Number of Completed Courses for Users in 10k AI Initiative",
    xaxis_title='User ID',
    yaxis_title='Completed Courses',
    hovermode='closest',
    showlegend=False
)

# Display the scatter plot in Streamlit
st.plotly_chart(fig_all_users_scatter, use_container_width=True)









#4
st.header(4)
#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM user_courses")

# Fetch and print the results


# st.header('Package of user_courses')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
user_courses = pd.DataFrame(result, columns=column_names)
# st.write(user_courses)



# Merge the two tables based on 'user_id' and 'course_id'
merged_data = user_courses.merge(user_completed_courses, on=['user_id', 'course_id'], how='left')

# Calculate the number of currently learning courses
merged_data['currently_learning_courses'] = 1
merged_data['currently_learning_courses'].fillna(0, inplace=True)
merged_data['completed_courses'] = merged_data['course_degree'].notna().astype(int)

# Calculate the number of completed courses during this week, month, and year
merged_data['completion_date'] = pd.to_datetime(merged_data['completion_date'])
this_week = merged_data[merged_data['completion_date'] >= pd.Timestamp('now') - pd.DateOffset(weeks=1)]
this_month = merged_data[merged_data['completion_date'] >= pd.Timestamp('now') - pd.DateOffset(months=1)]
this_year = merged_data[merged_data['completion_date'] >= pd.Timestamp('now') - pd.DateOffset(years=1)]

user_id = st.text_input("Enter the User ID: ")

if user_id:
    try:
        user_id = int(user_id)  # Convert the user ID to an integer

        # Filter the merged data based on the user_id
        user_data = merged_data[merged_data['user_id'] == user_id]

        if not user_data.empty:
            total_learning_courses = user_data['currently_learning_courses'].sum()
            total_completed_courses = user_data['completed_courses'].sum()

            # Create a bar chart for the user
            fig = px.bar(x=['Currently Learning Courses', 'Completed Courses'], y=[total_learning_courses, total_completed_courses],
                         title=f'User {user_id}: Currently Learning vs Completed Courses',
                         labels={'y': 'Number of Courses'})

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(f"No data found for User {user_id}.")
    except ValueError:
        st.write("Invalid input. Please enter a valid User ID (a numeric value).")




# Merge completion data with course data
completion_course_df = user_completed_courses.merge(courses, on='course_id')

# Calculate the number of currently learning courses and completed courses
merged_data['currently_learning_courses'] = 1
merged_data['currently_learning_courses'].fillna(0, inplace=True)
merged_data['completed_courses'] = merged_data['course_degree'].notna().astype(int)

# Group data by user and sum the number of currently learning and completed courses
user_summary = merged_data.groupby('user_id').agg(
    total_learning_courses=('currently_learning_courses', 'sum'),
    total_completed_courses=('completed_courses', 'sum')
).reset_index()

# Sort users by currently learning courses and total completed courses
sorted_users = user_summary.sort_values(by=['total_learning_courses', 'total_completed_courses'], ascending=[False, False])

# Display the sorted table
st.write(sorted_users)


#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM capstone_evaluation_history")

# Fetch and print the results


# st.header('Package of capstone_evaluation_history')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
capstone_evaluation_history = pd.DataFrame(result, columns=column_names)
# st.write(capstone_evaluation_history)





#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM users_employment_grant")

# Fetch and print the results


# st.header('Package of users_employment_grant')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
users_employment_grant = pd.DataFrame(result, columns=column_names)
# st.write(users_employment_grant)
#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM capstones")

# Fetch and print the results


# st.header('Package of capstones')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
capstones = pd.DataFrame(result, columns=column_names)
# st.write(capstones)



#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM user_lesson_history")

# Fetch and print the results


# st.header('Package of user_lesson_history')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
user_lesson_history = pd.DataFrame(result, columns=column_names)
# st.write(user_lesson_history)




#5
st.header(5)
#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM users_employment_grant_actions")

# Fetch and print the results


# st.header('Package of users_employment_grant_actions')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
users_employment_grant_actions = pd.DataFrame(result, columns=column_names)
# st.write(users_employment_grant_actions)

number = st.text_input('Enter your ID: ')

if number.isdigit():

    # Convert the input to an integer if necessary
    number = int(number) if number.isdigit() else number

    # Filter user-related data based on the user ID
    user_info = users[users['user_id'] == number]

    # Check if user_info is empty (no user with the given ID)
    if user_info.empty:
        st.write("No user found with the provided user ID.")
    else:
        # Filter bundles, capstones, completed courses, user courses, and lesson history data
        bundles_info = bundles[bundles['user_id'] == number]
        capstone_eval_history_info = capstone_evaluation_history[capstone_evaluation_history['user_id'] == number]
        capstones_info = capstones[capstones['user_id'] == number]
        completed_courses_info = user_completed_courses[user_completed_courses['user_id'] == number]
        user_courses_info = user_courses[user_courses['user_id'] == number]
        lesson_history_info = user_lesson_history[user_lesson_history['user_id'] == number]
        capstone_eval_history_info['degree'] = capstone_eval_history_info['degree'].astype(str)
        # Convert the "course_id" column to strings before concatenation
        capstones_info['course_id'] = capstones_info['course_id'].astype(str)
        completed_courses_info['course_id']=completed_courses_info['course_id'].astype(str)
        user_courses_info["course_id"]=user_courses_info['course_id'].astype(str)
        lesson_history_info["lesson_id"]=lesson_history_info['lesson_id'].astype(str)

        # Merge all the data into a single DataFrame
        merge_data = user_info.copy()
        merge_data['Bundles'] = bundles_info['bundle_name'].str.cat(sep=', ')
        merge_data['Capstones'] = capstones_info['course_id'].apply(str).str.cat(sep=', ')
        merge_data['Completed Courses'] = completed_courses_info['course_id'].apply(str).str.cat(sep=', ')
        merge_data['Degrees'] = capstone_eval_history_info['degree'].apply(str).str.cat(sep=', ')
        merge_data['Courses'] = user_courses_info['course_id'].apply(str).str.cat(sep=', ')
        merge_data['Lesson History'] = lesson_history_info['lesson_id'].apply(str).str.cat(sep=', ')

         # Select only the columns you want to display
        columns_to_display = ['user_id', 'Bundles', 'Capstones', 'Completed Courses', 'Degrees', 'Courses', 'Lesson History']
        merge_data = merge_data[columns_to_display]

        # Display the merged data
        st.write(merge_data)
else:
        st.write("Invalid input. Please enter a valid User ID (a numeric value).")


# Filter user-related data (no specific user ID provided)
user_info = users.copy()

# Filter bundles, capstones, completed courses, user courses, and lesson history data
bundles_info = bundles.copy()
capstone_eval_history_info = capstone_evaluation_history.copy()
capstones_info = capstones.copy()
completed_courses_info = user_completed_courses.copy()
user_courses_info = user_courses.copy()
lesson_history_info = user_lesson_history.copy()

capstone_eval_history_info['degree'] = capstone_eval_history_info['degree'].astype(str)
# Convert the "course_id" column to strings before concatenation
capstones_info['course_id'] = capstones_info['course_id'].astype(str)
completed_courses_info['course_id'] = completed_courses_info['course_id'].astype(str)
user_courses_info['course_id'] = user_courses_info['course_id'].astype(str)
lesson_history_info['lesson_id'] = lesson_history_info['lesson_id'].astype(str)

# Merge all the data into a single DataFrame
merge_data = user_info.copy()
merge_data['Bundles'] = bundles_info.groupby('user_id')['bundle_name'].apply(', '.join)
merge_data['Capstones'] = capstones_info.groupby('user_id')['course_id'].apply(', '.join)
merge_data['Completed Courses'] = completed_courses_info.groupby('user_id')['course_id'].apply(', '.join)
merge_data['Degrees'] = capstone_eval_history_info.groupby('user_id')['degree'].apply(', '.join)
merge_data['Courses'] = user_courses_info.groupby('user_id')['course_id'].apply(', '.join)
merge_data['Lesson History'] = lesson_history_info.groupby('user_id')['lesson_id'].apply(', '.join)

         # Select only the columns you want to display
columns_to_display = ['user_id', 'Bundles', 'Capstones', 'Completed Courses', 'Degrees', 'Courses', 'Lesson History']
merge_data = merge_data[columns_to_display]

        # Display the merged data
st.write(merge_data)








#6
st.header(6)
#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM capstone_evaluation_history")

# Fetch and print the results


# st.header('Package of capstone_evaluation_history')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
capstone_evaluation_history = pd.DataFrame(result, columns=column_names)
# st.write(capstone_evaluation_history)

# Convert evaluation_date to a datetime object
capstone_evaluation_history['evaluation_date'] = pd.to_datetime(capstone_evaluation_history['evaluation_date'])

# Extract day, week, month, and year information
capstone_evaluation_history['Day'] = capstone_evaluation_history['evaluation_date'].dt.date
capstone_evaluation_history['Week'] = capstone_evaluation_history['evaluation_date'].dt.strftime('%Y-%U')
capstone_evaluation_history['Month'] = capstone_evaluation_history['evaluation_date'].dt.strftime('%Y-%m')
capstone_evaluation_history['Year'] = capstone_evaluation_history['evaluation_date'].dt.year

# Create a Streamlit dashboard

st.header("Number of Capstones Evaluated by Each Admin")

# Create a multiselect dropdown for selecting period
selected_period = st.multiselect("Select Period:", ["Daily", "Weekly", "Monthly", "Yearly"])

# Calculate the number of capstones evaluated by each admin for the selected period(s)
counts = {}

if "Daily" in selected_period:
    daily_count = capstone_evaluation_history.groupby(['admin_id', 'Day']).size().reset_index(name='count_daily')
    counts['daily'] = daily_count

if "Weekly" in selected_period:
    weekly_count = capstone_evaluation_history.groupby(['admin_id', 'Week']).size().reset_index(name='count_weekly')
    counts['weekly'] = weekly_count

if "Monthly" in selected_period:
    monthly_count = capstone_evaluation_history.groupby(['admin_id', 'Month']).size().reset_index(name='count_monthly')
    counts['monthly'] = monthly_count

if "Yearly" in selected_period:
    yearly_count = capstone_evaluation_history.groupby(['admin_id', 'Year']).size().reset_index(name='count_yearly')
    counts['yearly'] = yearly_count

# Merge counts into one DataFrame
if counts:
    all_counts = pd.DataFrame({'admin_id': capstone_evaluation_history['admin_id'].unique()})

    for period, count_df in counts.items():
        count_df.rename(columns={'count': f'count_{period.lower()}'}, inplace=True)
        all_counts = pd.merge(all_counts, count_df, on='admin_id', how='left')

    # Fill NaN values with 0 for each period individually
    for period in counts.keys():
        all_counts[f'count_{period.lower()}'] = all_counts[f'count_{period.lower()}'].fillna(0)

    # Create the table with daily, weekly, monthly, and yearly counts
    st.write("Course Completion Summary:")
    st.table(all_counts[['admin_id'] + [f'count_{period.lower()}' for period in counts.keys()]])

    # Create the bar chart with daily, weekly, monthly, and yearly counts
    fig = px.bar(all_counts, x='admin_id', y=[f'count_{period.lower()}' for period in counts.keys()],
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 labels={"value": "Number of Capstones", "variable": "Period"},
                 title="Course Completion Summary")
    
    # Display the chart
    st.plotly_chart(fig)
else:
    st.warning("Please select at least one period.")






#7   
#----------------------------------------------------------------------------------
st.header(7)
# Get user input for the user ID
user_ided = st.text_input("Enter the User ID : ")

# Validate the user ID input
if user_ided.isdigit():
    user_ided = int(user_ided)  # Convert the user ID to an integer
    # Filter the evaluation history data for the specified user ID
    user_data = capstone_evaluation_history[capstone_evaluation_history['user_id'] == user_ided]

    # Check if user data is empty
    if user_data.empty:
        st.write("User has no capstone or evaluation history.")
    else:
        # Display the table with evaluation history
        st.write("Evaluation History for User", user_ided)
        st.table(user_data[['eval_history_id', 'admin_id', 'user_id', 'course_id', 'chapter_id', 'lesson_id', 'degree', 'evaluation_date']])
        
        # Create the interactive graph using Plotly
        fig = px.scatter(user_data, x='evaluation_date', y='degree', color='course_id', hover_data=['chapter_id', 'lesson_id'])
        fig.update_layout(title=f"Capstone and Evaluation History for User {user_ided}",
                          xaxis_title='Evaluation Date',
                          yaxis_title='Degree')

        # Display the interactive graph
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Invalid input. Please enter a valid User ID (a numeric value).")

# Filter the evaluation history data for users with history
users_with_evaluation_history = capstone_evaluation_history['user_id'].unique()

# Filter user-related data for users with evaluation history
user_info = users[users['user_id'].isin(users_with_evaluation_history)]

# Display the user information for those with evaluation history
st.write(capstone_evaluation_history)








#------------------------------------------
#8
st.header(8)
#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM copons")

# Fetch and print the results


# st.header('Package of copons')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
copons = pd.DataFrame(result, columns=column_names)
# st.write(copons)


# Prompt the user to enter a coupon ID
coupon_id = st.text_input("Enter the Coupon ID:")

# Check if the input is a valid number
if coupon_id.isdigit():
    coupon_id = int(coupon_id)

    # Join the user and copons tables on the appropriate columns
    merged_data = pd.merge(users, copons, left_on='coupon', right_on='copon_code')

    # Filter the merged data for the specified coupon ID
    coupon_users = merged_data[merged_data['coupon_id'] == coupon_id]

    # Check if there are users with the specified coupon ID
    if not coupon_users.empty:
        # Display the details of the users who used the coupon
        st.write(coupon_users)
    else:
        st.write(f"No users found with Coupon ID {coupon_id}")
else:
    st.write("Invalid input. Please enter a valid Coupon ID.")


st.write(copons)






#----------------------------
#9
st.header(9)
# Group users by age and study degree and count the number of users in each group
user_stats = users.groupby(['age', 'study_degree']).size().reset_index(name='count')

# Create an interactive bar chart to show user statistics
fig = px.bar(user_stats, x='age', y='count', color='study_degree',
             labels={'count': 'Number of Users'},
             title='Number of Users Grouped by Age and Study Degree')
fig.update_layout(xaxis_title='Age', yaxis_title='Number of Users')

# Display the bar chart
st.plotly_chart(fig, use_container_width=True)






















# #----------------------------------------
# # Execute a SELECT query
# cursor.execute("SELECT * FROM admins")

# # Fetch and print the results


# st.header('Package of admins')
# result=cursor.fetchall()
# # Get the column names from the cursor description
# column_names = [desc[0] for desc in cursor.description]

# # Create a DataFrame
# df = pd.DataFrame(result, columns=column_names)
# st.write(df)














#----------------------------------------
# Execute a SELECT query
cursor.execute("SELECT * FROM capstones")

# Fetch and print the results


# st.header('Package of capstones')
result=cursor.fetchall()
# Get the column names from the cursor description
column_names = [desc[0] for desc in cursor.description]

# Create a DataFrame
capstones = pd.DataFrame(result, columns=column_names)
# st.write(capstones)






























#--------------------------------------------------------------------------
#10

st.header(10)

# Prompt the user to enter a user ID
user_id_input = st.text_input("Enter the User ID :")

# Check if the input is a valid number
if user_id_input.isdigit():
    user_id = int(user_id_input)

    # Fetch user information for the specified user ID
    user_info = users_employment_grant[users_employment_grant['user_id'] == user_id]

    # Check if the user with the specified ID exists
    if not user_info.empty:
        # Display the details of the user
        st.write(user_info)
    else:
        st.write(f"No user found with ID {user_id}")
else:
    st.write("Invalid input. Please enter a valid User ID.")









# Merge the two dataframes on 'user_id'
user_grant_data = users_employment_grant.merge(users_employment_grant_actions, on='user_id', how='left')

# Create a Streamlit app
# st.title("Employment Grant Status Dashboard")

# Display a table showing users and their employment grant status and history
# st.write("Employment Grant Status and History")
# st.dataframe(user_grant_data)

# Calculate the number of users in each grant status
grant_status_counts = user_grant_data['status'].value_counts()

# Create a bar chart to show the number of users in each grant status
fig = px.bar(x=grant_status_counts.index, y=grant_status_counts.values, labels={'x': 'Status', 'y': 'Number of Users'},
             title='Number of Users in Each Employment Grant Status')
fig.update_xaxes(categoryorder='total descending')

# Display the bar chart
# st.write("Number of Users in Each Employment Grant Status")
st.plotly_chart(fig, use_container_width=True)
st.write (users_employment_grant)

cursor.close()
connection.close()