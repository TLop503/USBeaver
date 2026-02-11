#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

#define SDA_PIN 12     // D6 - OLED SDA
#define SCL_PIN 14     // D5 - OLED SCL

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Access Point credentials
const char* ssid = "usbeaver";
const char* password = "skobeavs";

ESP8266WebServer server(80);

int clientsConnected = 0;
String lastCommand = "None";

void setup() {
	Serial.begin(115200);  // UART to Pico

	Wire.begin(SDA_PIN, SCL_PIN);

	if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
		for(;;);
	}

	// Start Access Point
	WiFi.mode(WIFI_AP);
	WiFi.softAP(ssid, password);

	IPAddress IP = WiFi.softAPIP();

	// Display AP info
	displayStatus("Starting AP...", 0);
	delay(1000);

	// Setup web server routes
	server.on("/", handleRoot);
	server.on("/send", handleSend);
	server.on("/status", handleStatus);
	server.begin();

	displayStatus("Ready", WiFi.softAPgetStationNum());
}

void loop() {
	server.handleClient();

	// Update display periodically
	static unsigned long lastUpdate = 0;
	if(millis() - lastUpdate > 1000) {
		clientsConnected = WiFi.softAPgetStationNum();
		displayStatus("Ready", clientsConnected);
		lastUpdate = millis();
	}
}

void handleRoot() {
	String html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>USBeaver Control</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 600px;
      margin: 50px auto;
      padding: 20px;
      background: #1a1a1a;
      color: #fff;
    }
    h1 {
      color: #4CAF50;
      text-align: center;
    }
    .container {
      background: #2a2a2a;
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 20px;
    }
    textarea {
      width: 100%;
      height: 100px;
      padding: 10px;
      margin: 10px 0;
      border: 2px solid #4CAF50;
      border-radius: 5px;
      background: #1a1a1a;
      color: #fff;
      font-size: 16px;
      box-sizing: border-box;
    }
    button {
      background: #4CAF50;
      color: white;
      padding: 12px 24px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
      margin: 5px;
      width: calc(50% - 10px);
    }
    button:hover {
      background: #45a049;
    }
    .btn-danger {
      background: #f44336;
    }
    .btn-danger:hover {
      background: #da190b;
    }
    .script-btn {
      width: calc(33.33% - 10px);
      margin: 5px;
      padding: 10px;
      font-size: 14px;
    }
    #status {
      padding: 10px;
      background: #1a1a1a;
      border-radius: 5px;
      margin-top: 10px;
      color: #4CAF50;
    }
    .combo-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
gap: 10px;
}
</style>
</head>
<body>
<h1>USBeaver</h1>

<div class="container">
<h3>Type Text</h3>
<textarea id="textInput" placeholder="Enter text to type..."></textarea>
<button onclick="sendText()">Send Text</button>
<button onclick="clearText()">Clear</button>
</div>

<div class="container">
<h3>Quick Scripts</h3>
<div class="combo-grid">
<button class="script-btn" onclick="sendScript(0)">Hello World</button>
<button class="script-btn" onclick="sendScript(1)">Open Notepad</button>
<button class="script-btn" onclick="sendScript(2)">Open CMD</button>
<button class="script-btn" onclick="sendScript(3)">Task Manager</button>
<button class="script-btn" onclick="sendScript(4)">Lock PC</button>
<button class="script-btn" onclick="sendScript(5)">Custom</button>
</div>
</div>

<div class="container">
<h3>Key Combinations</h3>
<div class="combo-grid">
<button onclick="sendCombo('CTRL+C')">Copy</button>
<button onclick="sendCombo('CTRL+V')">Paste</button>
<button onclick="sendCombo('CTRL+Z')">Undo</button>
<button onclick="sendCombo('CTRL+A')">Select All</button>
<button onclick="sendCombo('ALT+F4')">Alt+F4</button>
<button onclick="sendCombo('CTRL+ALT+DEL')">Ctrl+Alt+Del</button>
<button onclick="sendCombo('GUI+R')">META+R</button>
</div>
</div>

<div class="container">
<h3>Special Keys</h3>
<div class="combo-grid">
<button onclick="sendKey('ENTER')">Enter</button>
<button onclick="sendKey('TAB')">Tab</button>
<button onclick="sendKey('ESC')">Escape</button>
<button onclick="sendKey('BACKSPACE')">Backspace</button>
<button onclick="sendKey('DEL')">Delete</button>
<button onclick="sendKey('SPACE')">Space</button>
<button onclick="sendKey('GUI')">Gui</button>
</div>
</div>

<div id="status">Status: Ready</div>

<script>
function sendCommand(cmd) {
	fetch('/send?cmd=' + encodeURIComponent(cmd))
		.then(response => response.text())
		.then(data => {
				document.getElementById('status').innerText = 'Status: ' + data;
				})
	.catch(error => {
			document.getElementById('status').innerText = 'Error: ' + error;
			});
}

function sendText() {
	var text = document.getElementById('textInput').value;
	if(text) {
		sendCommand('TYPE:' + text);
	}
}

function clearText() {
	document.getElementById('textInput').value = '';
}

function sendKey(key) {
	sendCommand('KEY:' + key);
}

function sendCombo(combo) {
	sendCommand('COMBO:' + combo);
}

function sendScript(num) {
	switch(num) {
		case 0:
			sendCommand('TYPE:Hello from Rubber Ducky!');
			setTimeout(() => sendCommand('KEY:ENTER'), 100);
			break;
		case 1:
			sendCommand('COMBO:GUI+R');
			setTimeout(() => sendCommand('TYPE:notepad'), 500);
			setTimeout(() => sendCommand('KEY:ENTER'), 1000);
			break;
		case 2:
			sendCommand('COMBO:GUI+R');
			setTimeout(() => sendCommand('TYPE:cmd'), 500);
			setTimeout(() => sendCommand('KEY:ENTER'), 1000);
			break;
		case 3:
			sendCommand('COMBO:CTRL+SHIFT+ESC');
			break;
		case 4:
			sendCommand('COMBO:GUI+L');
			break;
		case 5:
			// Custom script - modify as needed
			sendCommand('TYPE:Custom script here');
			break;
	}
}
</script>
</body>
</html>
)rawliteral";

server.send(200, "text/html", html);
}

void handleSend() {
	if(server.hasArg("cmd")) {
		String command = server.arg("cmd");
		lastCommand = command;

		// Send command to Pico via Serial
		Serial.println(command);

		// Update display
		displayStatus("Sent: " + command.substring(0, 10), clientsConnected);

		server.send(200, "text/plain", "Command sent: " + command);
	} else {
		server.send(400, "text/plain", "No command provided");
	}
}

void handleStatus() {
	String json = "{\"clients\":" + String(clientsConnected) + 
		",\"lastCommand\":\"" + lastCommand + "\"}";
	server.send(200, "application/json", json);
}

void displayStatus(String status, int clients) {
	display.clearDisplay();
	display.setTextSize(1);
	display.setTextColor(SSD1306_WHITE);

	// Title
	display.setCursor(0, 0);
	display.setTextSize(2);
	display.println("USBeaver");

	// IP Address
	display.setTextSize(1);
	display.setCursor(0, 20);
	display.print("IP: ");
	display.println(WiFi.softAPIP());

	// SSID
	display.setCursor(0, 32);
	display.print("SSID: ");
	display.println(ssid);

	// Clients
	display.setCursor(0, 44);
	display.print("Clients: ");
	display.println(clients);

	// Status
	display.setCursor(0, 56);
	display.print(status.substring(0, 20));

	display.display();
}
