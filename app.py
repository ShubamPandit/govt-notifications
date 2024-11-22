from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Initialize the Flask app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch-notifications')
def fetch_jkpsc_notifications():
    url = 'https://www.jkpsc.nic.in/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    notifications = []

    for li in soup.select('ul.notificationnews li a[visible="true"]'):
        notifications.append({
            'title': li.text.strip(),
            'url': url + li['href'].strip(),
        })

    return jsonify({'notifications': notifications})

@app.route('/fetch-jkssb-notifications', methods=['GET'])
def fetch_jkssb_notifications():
    base_url = "https://jkssb.nic.in/"
    notifications_url = f"{base_url}Whatsnew.html"

    try:
        response = requests.get(notifications_url)
        response.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for all links within the body
        links = soup.find_all('a', class_='linkText')
        notifications = []

        for link in links:
            title = link.text.strip()
            relative_link = link.get('href')
            if relative_link:
                absolute_link = urljoin(base_url, relative_link.lstrip('../'))  # Handle relative paths
                notifications.append({"title": title, "url": absolute_link})

        # print(notifications)  # Debug output for testing
        return jsonify({"notifications": notifications})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch notifications"}), 500


@app.route('/fetch-jkbopee-notifications', methods=['GET'])

def fetch_jkbopee_notifications():
    base_url = "https://www.jkbopee.gov.in/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    notifications = []

    try:
        rows = soup.select('div#Div1 table tbody tr')
        for row in rows:
            link = row.find('a', class_='title')
            if link:
                title = link.text.strip()
                relative_link = link.get('href')
                absolute_link = urljoin(base_url, relative_link)
                notifications.append({"title": title, "url": absolute_link})
                print("RL",relative_link)
                print("AL",absolute_link)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch JKBOPEE notifications"}), 500

    return jsonify({"notifications": notifications})

if __name__ == '__main__':
    app.run(debug=True)