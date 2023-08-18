#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from smartsheet import Smartsheet
from dateutil import parser
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
import numpy as np
from dash import Dash, dcc, html, Input, Output
import dash


# In[2]:


today = datetime.date.today()
year = today.year


# In[3]:


def get_report(report_id):
    smartsheet_client = Smartsheet('YOUR SMARTSHEET API')
    report = smartsheet_client.Reports.get_report(report_id, page_size=300000)
    rows = report.rows
    columns = report.columns

    # Extract column names
    column_names = [column.title for column in columns]

    # Extract row data and handle date format
    rows_data = []
    for row in rows:
        row_data = []
        for cell in row.cells:
            if isinstance(cell.value, str):
                try:
                    cell_value = parser.parse(cell.value)
                except ValueError:
                    try:
                        cell_value = int(cell.value)  # Try to convert to integer
                    except ValueError:
                        cell_value = cell.display_value
                except OverflowError:
                    cell_value = cell.display_value
            else:
                cell_value = cell.display_value

            row_data.append(cell_value)
        rows_data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(rows_data, columns=column_names)

    return df


# In[4]:


bucket_df = get_report(SMARTSHEET ID - INTEGER)


# In[5]:


completed_bucket = get_report(SMARTSHEET ID - INTEGER)


# In[6]:


returned_bucket = get_report(SMARTSHEET ID - INTEGER)


# In[7]:


def create_nmp_trace(bucket_df):
    bucket_df = bucket_df
    assignment_pivot_df = bucket_df.pivot_table(values='Subscriber Name',index='Assigned NMP',aggfunc=np.count_nonzero).reset_index()
    assignment_pivot_df['Assigned NMP']= assignment_pivot_df['Assigned NMP'].str.split(',')
    assignment_pivot_df = assignment_pivot_df.explode('Assigned NMP')
    assignment_pivot_df = assignment_pivot_df[((assignment_pivot_df['Assigned NMP'].str.contains(r'nmp@'))==False)&((assignment_pivot_df['Assigned NMP'].str.contains(r'Network Management and Provisioning'))==False)]
    assignment_pivot_df = assignment_pivot_df.rename(columns={"Subscriber Name":"Tasks Count"})
    assignment_pivot_df = assignment_pivot_df.sort_values('Tasks Count',ascending=False).head(10)
    fig_nmp_engineer = go.Bar(x=assignment_pivot_df['Assigned NMP'], y=assignment_pivot_df['Tasks Count'], name='Tasks Count',text=assignment_pivot_df['Tasks Count'],textposition='auto')
    return fig_nmp_engineer
    
    


# In[8]:


completed_bucket_within_the_year = completed_bucket[completed_bucket['Date Completed by NMP'].dt.year==year]


# In[9]:


completed_value_w_d_year = len(completed_bucket_within_the_year['Subscriber Name'])


# In[10]:


pending_value = len(bucket_df.loc[bucket_df['NMP Status']=='Endorsed','NMP Status'])


# In[11]:


returned_value = len(returned_bucket['Subscriber Name'])


# In[12]:


def indicator_trace(completed_value_w_d_year,pending_value,returned_value):
    fig_indicator = go.Figure()
    
    fig_indicator.add_trace(go.Indicator(
        mode="number",
        value=completed_value_w_d_year + pending_value + returned_value,
        title={"text": "Total<br>"},
        domain={'row': 0, 'column': 0}))

    fig_indicator.add_trace(go.Indicator(
        mode="number",
        value=returned_value,
        title={"text": "Returned<br>"},
        domain={'row': 0, 'column': 1}))

    fig_indicator.add_trace(go.Indicator(
        mode="number",
        value=completed_value_w_d_year,
        title={"text": "Completed<br>"},
        domain={'row': 0, 'column': 2}))

    fig_indicator.add_trace(go.Indicator(
        mode="number",
        value=pending_value,
        title={"text": "Pending<br>"},
        domain={'row': 0, 'column': 3}))

    fig_indicator.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"},)
    return fig_indicator
    


# In[13]:


def pie_trace(returned_value,completed_value_w_d_year,pending_value):
    pie_values = [returned_value,completed_value_w_d_year,pending_value]
    pie_status=['Returned','Completed','Pending']
    data = {'Value': pie_values, 'Status': pie_status}
    pie_df = pd.DataFrame(data)
    pie_fig = go.Pie(labels=pie_df['Status'], values=pie_df['Value'])
    return pie_fig
    


# In[14]:


def second_row_trace(bucket_df,returned_value,completed_value_w_d_year,pending_value):
    combined_graph_subfig = make_subplots(rows=1, cols=2,specs=[[{"type": "bar"}, {"type": "pie"}]],subplot_titles=["NMP Engineer Tasks", "Task Status Distribution"])
    combined_graph_subfig.add_trace(create_nmp_trace(bucket_df),row=1,col=1)
    combined_graph_subfig.add_trace(pie_trace(returned_value,completed_value_w_d_year,pending_value),row=1,col=2)
    return combined_graph_subfig


# In[15]:


def seven_days_completion(completed_bucket):
    seven_days_ago = datetime.datetime.today() - datetime.timedelta(days=7)
    completed_seven_days_ago = completed_bucket[completed_bucket['Date Completed by NMP']>=seven_days_ago]
    completed_seven_days_ago_df = completed_seven_days_ago.pivot_table(values='Subscriber Name',index='Date Completed by NMP',aggfunc='count').rename(columns={'Subscriber Name':'Count'}).reset_index()
    completed_seven_days_ago_trace = go.Bar(x=completed_seven_days_ago_df['Date Completed by NMP'], y=completed_seven_days_ago_df['Count'], name='Daily Completed Task History',text=completed_seven_days_ago_df['Count'],textposition='auto')
    return completed_seven_days_ago_trace
    


# In[16]:


def montly_completion_trace(completed_value_w_d_year):
    completed_bucket_within_the_year['Month']=completed_bucket_within_the_year['Date Completed by NMP'].dt.month_name()
    completed_bucket_within_the_year['Month_No']=completed_bucket_within_the_year['Date Completed by NMP'].dt.month
    completed_bucket_within_the_year['Month'] = "("+completed_bucket_within_the_year['Month_No'].astype(str)+")"+ completed_bucket_within_the_year['Month']
    year_to_date_completed = completed_bucket_within_the_year.pivot_table(values='Subscriber Name',index='Month',aggfunc='count').rename(columns={'Subscriber Name':'Count'}).reset_index()
    year_to_date_completed['Month'] = year_to_date_completed['Month'].str.extract(r'\)(.+)')
    completed_montly_for_current_year_trace = go.Bar(x=year_to_date_completed['Month'], y=year_to_date_completed['Count'], name='Completed Monthly',text=year_to_date_completed['Count'],textposition='auto')
    return completed_montly_for_current_year_trace


# In[17]:


def third_row_trace(completed_bucket,completed_value_w_d_year):
    combined_graph_subfig_2 = make_subplots(rows=1, cols=2,specs=[[{"type": "bar"}, {"type": "bar"}]],subplot_titles=["Daily Completed Task History", "Monthly Completed Tasks"])
    combined_graph_subfig_2.add_trace(seven_days_completion(completed_bucket),row=1,col=1)
    combined_graph_subfig_2.add_trace(montly_completion_trace(completed_value_w_d_year),row=1,col=2)
    return combined_graph_subfig_2


# In[18]:


app = Dash(__name__)


# In[19]:


app.layout = html.Div(children=[
    html.H1(children='Service Delivery Dashboard'),
    
    dcc.Graph(
        id='graph_indicator',
        figure=indicator_trace(completed_value_w_d_year,pending_value,returned_value)
    ),
    
   
    dcc.Graph(
            id='second_row_trace',
            figure=second_row_trace(bucket_df,returned_value,completed_value_w_d_year,pending_value)
        ),
     dcc.Graph(
            id='graph_task_completed',
            figure=third_row_trace(completed_bucket,completed_value_w_d_year)
        ),   
    # JavaScript to reload the page every 15 minutes
    dcc.Interval(
        id='interval-component',
        interval=15*60*1000,  # in milliseconds
        n_intervals=0
    )
    
])


# In[20]:


# Define a callback function to update the data and layout
@app.callback(
    [dash.dependencies.Output('graph_indicator', 'figure'),
     dash.dependencies.Output('second_row_trace', 'figure'),
     dash.dependencies.Output('graph_task_completed', 'figure')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_data_and_layout(n_intervals):
    # Fetch updated data from Smartsheet
    bucket_df = get_report(7163404709324676)
    completed_bucket = get_report(1990309172957060)
    returned_bucket = get_report(7410351742078852)

    # Update global variables or store data in a session for other callbacks to use
    completed_bucket_within_the_year = completed_bucket[completed_bucket['Date Completed by NMP'].dt.year==year]
    completed_value_w_d_year = len(completed_bucket_within_the_year['Subscriber Name'])
    pending_value = len(bucket_df.loc[bucket_df['NMP Status']=='Endorsed','NMP Status'])
    returned_value = len(returned_bucket['Subscriber Name'])
    
    # Update the figures for the first, second, and third rows
    indicator_fig = indicator_trace(completed_value_w_d_year, pending_value, returned_value)
    second_row_fig = second_row_trace(bucket_df, returned_value, completed_value_w_d_year, pending_value)
    third_row_fig = third_row_trace(completed_bucket, completed_value_w_d_year)

    return indicator_fig, second_row_fig, third_row_fig


# In[21]:


if __name__ == '__main__':
    # Run the app on port 9000
    print("Created by Dennis A. Garcia")
    app.run_server(debug=False, port=9000)
    input("Press Enter to Exit")




