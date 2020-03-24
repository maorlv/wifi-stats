"""
Maor Levy
@ https://github.com/redspade91
2020
"""

import subprocess, threading, re, socket, os, logging
from flask import Flask, jsonify

# define ip and port to be used in app
IP, PORT = socket.gethostbyname(socket.gethostname()), 8000
app = Flask(__name__, static_url_path='')

# Get the server up
def srv():
	os.environ['WERKZEUG_RUN_MAIN'] = 'true'
	logging.getLogger('werkzeug').disabled = True

	print("\nServer is up!\nWhen you're done, close this window or press <ENTER> again to shut down the server.")

	app.run(host='0.0.0.0', port=PORT, debug=None)		

# write stats to be read by index.html
@app.route('/stats', methods=['GET'])
def netsh():

	# get info
	netshcap = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True)
	output = netshcap.stdout.decode()

	try:
		ssid = output.split("SSID")[1].split("\r\n")[0].replace(":", "").strip()
		values = re.findall(r"([0-9\.]+)", output.split("Transmit")[1])
	except:
		ssid, values = "DISCONNECTED", [0, 0]

	# update file only on changes
	return jsonify([ssid, values[0], values[1]])
		

@app.route('/', methods=['GET'])
def root():
	return app.send_static_file('index.html')


if __name__ == "__main__":
	print(f"To view WiFi stats of this computer on another device, make sure that both the device and the computer are connected to the same WiFi network.\nThe app will be accessible at http://{IP}:{PORT}/ after you'll start the server.")
	input("\nPress <ENTER> to start server.")
	
	# start the server and the file-reader in two different threads. both threads will be killed when main application is done (after next input)
	threads = [threading.Thread(target=srv, daemon=True)]
	[trd.start() for trd in threads]

	# any input to exit
	input()

	print("Goodbye :)")