# Service Delivery Dashboard


This is a service delivery dashboard built using Python's Dash framework and Plotly for data visualization. The dashboard displays key metrics related to service delivery tasks and provides insights into task distribution, completion rates, and more.

## Features

- Real-time data updates from Smartsheet API
- Visual representation of task distribution among Network Management and Provisioning (NMP) engineers
- Overview of task status (Completed, Pending, Returned)
- Daily and monthly trends in completed tasks
- Automatic refresh of data every 15 minutes

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/service-delivery-dashboard.git

Install the required packages using pip:

bash
Copy code
pip install -r requirements.txt
Replace 'YOUR SMARTSHEET API' with your actual Smartsheet API key in the service_delivery_dashboard.py file.

Usage
Navigate to the project directory:

bash
Copy code
cd service-delivery-dashboard
Run the dashboard:

bash
Copy code
python service_delivery_dashboard.py
Access the dashboard in your web browser by visiting http://127.0.0.1:9000.

The dashboard will automatically update data every 15 minutes. You can also manually refresh the page.


#Credits
Built by Dennis A. Garcia
Smartsheet API integration using the Smartsheet Python SDK
Developed using Python's Dash and Plotly

License
This project is licensed under the MIT License.








