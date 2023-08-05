from flask import Flask
from threading import Thread
app = Flask('hoster')
@app.route('/')
def main():
  return "Your code has been hosted!"
def start(ip='0.0.0.0', port=8080):
    def run():
        app.run(host=ip, port=port)
    server = Thread(target=run)
    server.start()