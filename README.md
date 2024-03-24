# Flask Planner App

This Flask Planner App is a web application that allows users to create and manage their weekly plans. It features a user authentication system, a dynamic weekly planner with 24-hour segmentation, and utilizes HTMX for seamless partial page updates.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
* Python 3.8 or above
* Flask 1.1.2 or above
* HTMX for front-end interactions
* Tailwind CSS for styling

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/flask-planner-app.git
cd flask-planner-app
```

### Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Configuration
Create a .env file in the root directory and add your environment variables:

```python
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### Running the Application
To run the Flask application, use the following commands:

```python
flask run
```

The application will be available at http://127.0.0.1:5000/.
### 
Debugging
If you encounter any issues, you can enable debug mode to get detailed error logs:

```python
export FLASK_ENV=development
flask run
```

### Features
- User authentication (login and registration)
- Dynamic weekly planner grid
- Hourly segmentation for each day of the week
- Partial page loads using HTMX
- Styling with Tailwind CSS

### Contributing
We welcome contributions to the Flask Planner App. Please read our CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

### Authors
Suresh Babu - Initial work - sureshbabudj

### License
This project is licensed under the MIT License - see the LICENSE.md file for details.
