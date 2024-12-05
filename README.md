# FINANCIAL PLANNER AND MANAGEMENT SYSTEM

## Problem Idea 
Implement a financial planner and management systems that allows users to track income, expenses, and budget.   
 
## Project Features 

 User signup and login 

 Track income and expenses 

 Create a budget with different categories 

 Generate reports such as spending habits, income history 

 
## Databases 
SQLITE 3
 
## Technology Stack 
### Backend: python, flask 
### Frontend: HTML, CSS, JS 

## System Design
### FrontEnd User Interface 

- Built by using HTML, CSS and JavaScript
* The User Interface interacts with forms, buttons, and navigation menus to perform tasks like signup, login, adding budgets, and generating reports.

### Backend

- Built with Flask (a Python web framework).
* Handles requests from the user, processes data, interacts with the database, and sends responses back to the frontend.

### Database 

- Uses SQLite3 as the database to store all the data, such as user information, budgets, income, expenses, and categories.

### Deployment

- The app is deployed on Microsoft Azure, which provides a cloud platform for hosting the application and making it accessible online.


## Data Workflow 
Here’s a simple flow of how data moves between the components:

1.User Interaction (Frontend):
- The user interacts with forms, buttons, and navigation links.
2. Requests to Backend:
* The frontend sends user inputs (e.g., signup details, income data) to the backend via HTTP requests.
3. Backend Processing:
+ The Flask backend receives the request, processes it, and interacts with the database to fetch or store data.
4. Database Operations:
- The SQLite3 database stores and retrieves data for users, budgets, income, and expenses.
5. Response to Frontend:
* The backend sends the processed data or confirmation back to the frontend (e.g., "Signup successful!").
+ The frontend updates the UI with the new information.

## Screenshot of the deployed Web Application

<img width="1440" alt="Screenshot 2024-12-05 at 10 43 16 AM" src="https://github.com/user-attachments/assets/7fe64b1d-b8db-4100-a897-fc5e7b93e75b">

