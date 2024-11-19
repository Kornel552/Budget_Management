# Budget_Management
> Application to control your expenses

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Setup](#setup)

## General Information
- The main purpose of this project is to track and increase awareness of personal expenses.
- The application divides expenses by people and categories, allowing for better control.
- The project also include charts that help visualize expenses over a given period.

## Technologies Used
- Python - version 3.11
- Django - version 5.1.3
- Bootstrap - version 4.3.1
- HTML/CSS (for HTML templates and preview)

## Setup
1. Clone the repository to your local machine.
2. Install the required dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```
3. Activate the virtual environment in the appropriate path:
   ```
   .\activate
   ```
4. Apply migrations to set up the database:
   ```
   py manage.py makemigrations
   ```
5. Migrate to create the tables and SQLite database:
   ```sh
   py manage.py migrate
   ```
6. Run application:
   ```
   py manage.py runserver
   ```

