from flask import Flask, request
import subprocess
from subprocess import Popen
import schedule
import time
appFlask = Flask(__name__)

unit = ""

def take_photo():
    subprocess.call("termux-camera-photo -c 0 " + unit + ".jpg", shell=True)
    subprocess.call("./scp.sh")

@appFlask.route("/", methods=["GET", "POST"])
def main():
    if(request.method == "POST"):
        unit = request.form.get('unit')
        unitNumber = unit.split(";")
        unit = unitNumber[0]
        timestamp = unitNumber[1]
        print(timestamp)

        schedule.every().day.at(timestamp).do(take_photo)

        while True:
            schedule.run_pending()
            time.sleep(1)

    return "[PHOTO TAKEN]"

if __name__ == "__main__":
    appFlask.run(host="0.0.0.0",port=5000,debug=True)