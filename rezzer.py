from flask import Flask, request
import subprocess
from subprocess import Popen
appFlask = Flask(__name__)

@appFlask.route("/", methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        content = request.get_json(silent=False)
        unit_number = content['unitName'] # Do your processing
        subprocess.call("termux-camera-photo -c 0 " + unit_number + ".jpg", shell=True)
        subprocess.call("./scp.sh")
        return "Submitted!"

    return '''
<input type="button" value="UNIT 1" onclick="sendPost('1')" />
<script>
    var deviceIpAddresses = {};
    deviceIpAddresses["1"] = "http://192.168.1.123:5000";

    function sendPost(unitNumber){
        let xhr = new XMLHttpRequest();
        xhr.open("POST", deviceIpAddresses[unitNumber]);
        xhr.setRequestHeader("Accept", "application/json");
        xhr.setRequestHeader("Content-Type", "application/json");
        
        xhr.onreadystatechange = function () {
          if (xhr.readyState === 4) {
            console.log(xhr.status);
            console.log(xhr.responseText);
          }};
        
        var json_arr = {};
        json_arr["unitName"] = unitNumber;

        var json_string = JSON.stringify(json_arr);
        //let data = `{"unitNumber":""+unitNumber}`;
        
        xhr.send(json_string);
    }
</script>
              '''
if __name__ == "__main__":
    appFlask.run(host="0.0.0.0",port=5000,debug=True)