![AICAP LOGO](../frontend/src/Misc/logo-cover.png)

# Codeforces-Analytics Backend

Welcome to the backend repository of the Artificial Intelligence Codeforces Analytics Platform (AICAP). This backend component serves as the powerhouse of our platform, handling data processing, API integrations, and intelligent algorithms to deliver personalized insights and recommendations for competitive programmers. Below, you'll find essential information to understand, set up, and contribute to this backend system.

## Features:

1. **Data Integration:** Connects with the Codeforces API to gather user activity, contest details, and problem sets.

2. **Data Processing:** Implements algorithms to process and analyze user data, generating insightful charts and predictive models.

3. **API Endpoints:** Provides endpoints for frontend components to fetch processed data and predictions.

4. **Database Management:** Manages the SQL database(flexible, because it uses sqlalchemy), storing user profiles, solved problems, and contest-related information.

## Getting Started:

### Installation:

* Ensure you have Python installed on your system.
* Set up a virtual environment: python -m venv venv
* Activate the virtual environment: source venv/bin/activate (Linux/macOS) or venv\Scripts\activate (Windows)
* Install dependencies: pip install -r requirements.txt

### Configuration:
Set up the SQL database(the default is Postgresql) and configure the connection in config.py.

### Running the Backend:
Run the application:  ``` flask --app 'backend.app.app:create_app(DATABASE_CONNECTION_LINK)' run --debug ```. Make sure you're in the root folder.  
The backend server will start at http://localhost:5000.

### Testing
To run the unit tests use the following command ```pytest```.  
Make sure you're in the root folder

### API Endpoints:
* ```/users/<handle>```: Retrieve user details, including solved problems.
* ```/users/<handle> POST METHOD```: Update user details, including solved problems and contest history.
* ```/problems/<handle>```: Get the problems solved by the user.
* ```/recommend/<handle>?limit={number}```: Get personalized problem recommendations for a specific user. The ```limit``` argument is optional and it sets the number of recommended problems to be retrieved
* ```/predict/<handle>?rating={desired_rating}```: Predict the time required to achieve the desired Codeforces rating for a user. The ```rating``` argument is mandatory.
* ```/distribution/problems```: Get the solved problems distribution data for visualization.
* ```/distribution/rating```: Get the user rating distribution data for visualization.
* ```/migrate/problems```: Migrates the problems from the codeforces api to the database.
* ```/migrate/users```: Migrates the problems from the codeforces api to the database.
* ```/migrate/contests```: Migrates the problems from the codeforces api to the database.

## Contributing:

We welcome contributions to enhance the backend functionality of AICAP. Feel free to submit bug reports, feature requests, or pull requests to help us improve and expand the capabilities of our platform.

Thank you for your interest in the AICAP backend. Together, let's empower programmers with data-driven insights and foster growth in the competitive coding community. Happy coding!
