from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def main():
  return "Your code has been hosted!"
def start(ip, port):
    def run():
        app.run(host=ip, port=port)
    server = Thread(target=run)
    server.start()