# Flask-Blog
Made to learn Flask framework. Followed the incredible <a href="https://youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH"> tutorial series</a> by <a href="https://www.youtube.com/c/Coreyms">Corey Schafer</a>

## Getting Started

### Prerequisites
All the dependancies are listed in requirements.

### Installation
To install, first create a virtual environment and activate it.
```
python3 -m venv env_name
source env_name/bin/activate
```
If you have anaconda installed, create an environment using that.
```
conda create --name env_name python=[python version]  // 3.6 and over
```
**"env_name"** should contain the name of the environment. Then install all the packadges from the requirements.
```
pip install -r requirements.txt
```

### Setting environment variables
In this app a few sensitive information is hidden using environment variables such as:
```
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
MAIL_USERNAME = os.environ.get('EMAIL_USER')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
```
If there is some problem setting these up, please see <a href="https://youtu.be/IolxqkL7cD8">this video</a> for windows and <a href="https://youtu.be/5iWhQWVXosU">this video</a> for mac/linux.

### Running the app
Run this command on cmd
```
python app.py
```
It will run it on a local server. You can access it from any browser.
