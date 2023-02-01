from flask import Flask, request
import subprocess
from subprocess import Popen
appFlask = Flask(__name__)

@appFlask.route("/", methods = ['GET'])
def main():
    args = request.args
    unit = args.get("unit")
    subprocess.call("termux-camera-photo -c 0 " + unit + ".jpg", shell=True)
    subprocess.call("./scp.sh")
    return "[PHOTO TAKEN]"

if __name__ == "__main__":
    appFlask.run(host="0.0.0.0",port=5000,debug=True)