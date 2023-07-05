import requests
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)

def retrieve_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            if 'numbers' in data:
                return data['numbers']
    except requests.exceptions.RequestException:
        pass
    return []

@app.route('/numbers')
def get_numbers():
    urls = request.args.getlist('url')
    numbers = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(retrieve_numbers, url) for url in urls]
        for future in futures:
            numbers += future.result()
    numbers = sorted(list(set(numbers)))
    return jsonify({'numbers': numbers})

@app.route('/numbers/primes')
def get_prime_numbers():
    url = 'http://104.211.219.98/numbers/primes'
    return get_numbers_from_url(url)

@app.route('/numbers/fibo')
def get_fibonacci_numbers():
    url = 'http://104.211.219.98/numbers/fibo'
    return get_numbers_from_url(url)

@app.route('/numbers/odd')
def get_odd_numbers():
    url = 'http://104.211.219.98/numbers/odd'
    return get_numbers_from_url(url)

@app.route('/numbers/rand')
def get_random_numbers():
    url = 'http://104.211.219.98/numbers/rand'
    return get_numbers_from_url(url)

def get_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            if 'numbers' in data:
                numbers = data['numbers']
                return jsonify({'numbers': numbers})
    except requests.exceptions.RequestException:
        pass
    return jsonify({'numbers': []})

if __name__ == '__main__':
    app.run(debug=True)
