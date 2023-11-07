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
daily_users = users.groupby('Day').size().reset_index(name='Registered Users')
weekly_users = users.groupby('Week').size().reset_index(name='Registered Users')
monthly_users = users.groupby('Month').size().reset_index(name='Registered Users')
yearly_users = users.groupby('Year').size().reset_index(name='Registered Users')

subscribed_users = users[users['subscribed'] == 1].groupby('Day').size().reset_index(name='Subscribed Users')

# Create the figure and add traces
fig = go.Figure()

# Add traces for registered users
fig.add_trace(go.Scatter(x=daily_users['Day'], y=daily_users['Registered Users'], name='Daily Registered Users'))
fig.add_trace(go.Scatter(x=weekly_users['Week'], y=weekly_users['Registered Users'], name='Weekly Registered Users'))
fig.add_trace(go.Scatter(x=monthly_users['Month'], y=monthly_users['Registered Users'], name='Monthly Registered Users'))
fig.add_trace(go.Bar(x=yearly_users['Year'], y=yearly_users['Registered Users'], name='Yearly Registered Users'))

# Add trace for subscribed users
fig.add_trace(go.Scatter(x=subscribed_users['Day'], y=subscribed_users['Subscribed Users'], name='Daily Subscribed Users'))

# Set layout properties
fig.update_layout(title='Registered and Subscribed Users',
                  xaxis_title='Time Period',
                  yaxis_title='Number of Users')

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
# st.write(bundles)


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
    fig.add_trace(go.Scatter(x=daily_subscriptions[daily_subscriptions['bundle_name'] == bundle]['Day'],
                             y=daily_subscriptions[daily_subscriptions['bundle_name'] == bundle]['Subscribed Users'],
                             name=f'Daily Subscriptions - {bundle}'))

# Add traces for weekly subscriptions
for bundle in bundles['bundle_name'].unique():
    fig.add_trace(go.Scatter(x=weekly_subscriptions[weekly_subscriptions['bundle_name'] == bundle]['Week'],
                             y=weekly_subscriptions[weekly_subscriptions['bundle_name'] == bundle]['Subscribed Users'],
                             name=f'Weekly Subscriptions - {bundle}'))

# Add traces for monthly subscriptions
for bundle in bundles['bundle_name'].unique():
    fig.add_trace(go.Scatter(x=monthly_subscriptions[monthly_subscriptions['bundle_name'] == bundle]['Month'],
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

        # Create the interactive graph
        fig = go.Figure(data=[
            go.Bar(x=[user_id],
                   y=[len(user_completion_data)],
                   text=[last_completed_course['title']],
                   marker=dict(color='rgb(158,202,225)'),
                   hovertemplate=
                   '<b>User ID: %{x}</b><br>' +
                   'Completed Courses: %{y}<br>' +
                   'Last Completed Course: %{text}<br>' +
                   'Course Degree: %{customdata.course_degree}<br>' +
                   'Completion Date: %{customdata.completion_date}'
                   )
        ])

        # Add custom data (course degree and completion date) to the trace
        fig.data[0]['customdata'] = [{
            'course_degree': last_completed_course['course_degree'],
            'completion_date': last_completed_course['completion_date']
        }]

        # Set layout properties
        fig.update_layout(
            title=f"Last Completed Course for User {user_id}",
            xaxis_title='User ID',
            yaxis_title='Completed Courses',
            hovermode='closest',
            showlegend=False
        )

        # Display the graph in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write(f"User {user_id} is not in the 10k AI Initiative.")
else:
    st.write("Invalid input. Please enter a valid User ID.")










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

        # Display the merged data
        # print(merged_data)
        st.write(merge_data)
else:
        st.write("Invalid input. Please enter a valid User ID (a numeric value).")










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

# Calculate the number of capstones evaluated by each admin for today, this week, and this month
today = datetime.now()
this_week = today - pd.DateOffset(7)
this_month = today.replace(day=1)
this_year = today.replace(day=1, month=1)

today_count = capstone_evaluation_history[capstone_evaluation_history['evaluation_date'].dt.date == today.date()].groupby('admin_id').size().reset_index(name='count')
this_week_count = capstone_evaluation_history[capstone_evaluation_history['evaluation_date'] >= this_week].groupby('admin_id').size().reset_index(name='count')
this_month_count = capstone_evaluation_history[capstone_evaluation_history['evaluation_date'] >= this_month].groupby('admin_id').size().reset_index(name='count')
this_year_count = capstone_evaluation_history[capstone_evaluation_history['evaluation_date'] >= this_year].groupby('admin_id').size().reset_index(name='count')

# Combine all counts into one DataFrame
all_counts = pd.concat([today_count, this_week_count, this_month_count, this_year_count])
all_counts['period'] = ['Today'] * len(today_count) + ['This Week'] * len(this_week_count) + ['This Month'] * len(this_month_count) + ['This Year'] * len(this_year_count)

# Create the interactive Plotly bar chart
fig = px.bar(all_counts, x='admin_id', y='count', color='period', labels={"count": "Number of Capstones"})

# Create a Streamlit dashboard
# st.title("Admin Capstone Evaluation Dashboard")
# st.header("Number of Capstones Evaluated by Each Admin")

# Display the combined chart
st.plotly_chart(fig)










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
        # Create the interactive graph using Plotly
        fig = px.scatter(user_data, x='evaluation_date', y='degree', color='course_id', hover_data=['chapter_id', 'lesson_id'])
        fig.update_layout(title=f"Capstone and Evaluation History for User {user_ided}",
                          xaxis_title='Evaluation Date',
                          yaxis_title='Degree')

        # Display the interactive graph
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Invalid input. Please enter a valid User ID (a numeric value).")










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

    # Filter the coupon data for the specified coupon ID
    coupon_info = copons[copons['coupon_id'] == coupon_id]

    # Check if the coupon with the specified ID exists
    if not coupon_info.empty:
        # Display the details of the coupon
        st.write(coupon_info)
    else:
        st.write(f"No coupon found with ID {coupon_id}")
else:
    st.write("Invalid input. Please enter a valid Coupon ID.")









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








#--------------------------------------------------------------------------
#10

st.header(10)
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


cursor.close()
connection.close()

