from flask import Flask, request
import subprocess
from subprocess import Popen
import schedule
import time
appFlask = Flask(__name__)

def take_photo(unit):
    subprocess.call("termux-camera-photo -c 0 " + unit + ".jpg", shell=True)
    subprocess.call("./scp.sh")
    print("[PHOTO TAKEN]\n")

@appFlask.route("/", methods=["GET", "POST"])
def main():
    if(request.method == "GET"):
        unit = request.args.get('unit')
        timestamp = request.args.get('time')
        print("[Picture will be taken at: " + timestamp + "]\n")

        schedule.every().day.at(timestamp).do(take_photo, unit)

        while True:
            schedule.run_pending()
            time.sleep(1)

    if(request.method == "POST"):
        unit = request.form.get('unit')
        unitNumber = unit.split(";")
        unit = unitNumber[0]
        timestamp = unitNumber[1]
        print("[Picture will be taken at: " + timestamp + "]\n")

        schedule.every().day.at(timestamp).do(take_photo, unit)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    appFlask.run(host="0.0.0.0",port=5000,debug=True)