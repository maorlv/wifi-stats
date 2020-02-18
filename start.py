"""
Maor Levy
@ https://github.com/redspade91
2020
"""


import http.server, socket, socketserver, subprocess, threading, time, re

# define ip and port to be used in app
IP, PORT = socket.gethostbyname(socket.gethostname()), 8000

# stop making noise!!!
class QuietHandler(http.server.SimpleHTTPRequestHandler):
	def log_message(self, format, *args):
		pass

# Get the server up
def srv():
	Handler = QuietHandler
	with socketserver.TCPServer(("", PORT), Handler) as httpd:
		print("\nServer is up!\nWhen you're done, close this window or press <ENTER> again to shut down the server.")
		httpd.serve_forever()

# write stats to file to be read by index.html
def netsh():
	
	prev = ["", 0, 0]

	while True:
		# get info and write to file
		#subprocess.Popen('netsh wlan show interfaces', shell=True, stdout=f)
		netshcap = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True)
		output = netshcap.stdout.decode()

		try:
			ssid = output.split("SSID")[1].split("\r\n")[0].replace(":", "").strip()
			values = re.findall(r"([0-9\.]+)", output.split("Transmit")[1])
		except:
			ssid, values = "DISCONNECTED", [0, 0]

		# update file only on changes
		if [ssid, values[0], values[1]] != prev:
			f = open("stats.txt", "w")
			f.write("{},{},{}".format(ssid, values[0], values[1]))
			f.close()
			prev = [ssid, values[0], values[1]]
		
		# sleep for a second
		time.sleep(1)

if __name__ == "__main__":
	print(f"To view WiFi stats of this computer on another device, make sure that both the device and the computer are connected to the same WiFi network.\nThe app will be accessible at http://{IP}:{PORT}/ after you'll start the server.")
	input("\nPress <ENTER> to start server.")
	
	# start the server and the file-reader in two different threads. both threads will be killed when main application is done (after next input)
	threads = [threading.Thread(target=netsh, daemon=True), threading.Thread(target=srv, daemon=True)]
	[trd.start() for trd in threads]

	# any input to exit
	input()

	print("Goodbye :)")