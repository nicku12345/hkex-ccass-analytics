
FROM python:3

WORKDIR /HKEXAnalytics

COPY . /HKEXAnalytics

RUN pip install -r requirements.txt

# For Heroku deployment, specify explicitly the port to be 0.0.0.0:$PORT
# It is because Heroku randomly assigns a port to each deployment
# 0.0.0.0 here is needed to indicate that it binds to any port
# CMD gunicorn -b 0.0.0.0:$PORT 'mining:create_app()'

# For local deployment, simply use a fixed port ($PORT=5000) is fine
CMD gunicorn -b 0.0.0.0:5000 'hkex:create_app("PROD")'

# Deployment using waitress is not recommended.
# Waitress has a known issue where it will duplicate logging messages
# CMD waitress-serve --call --host="0.0.0.0" --port=5000 'hkex:create_app'