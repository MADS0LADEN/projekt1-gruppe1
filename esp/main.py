import asyncio
import socket

import network
from microdot import Microdot
from sensor import Alarm, Sensor

mac = ""


def reset_wifi_mode():
    try:
        ap = network.WLAN(network.AP_IF)
        mac = "".join(["%02x" % b for b in ap.config("mac")])
        ap.config(ssid=f"Lækagealarm-{mac[-4:]}")
        ap.config(max_clients=1)
        client = network.WLAN(network.STA_IF)
    except OSError as e:
        if str(e) == "Wifi Invalid Mode":
            print("Resetting WiFi mode...")
            network.WLAN(network.AP_IF).active(False)
            network.WLAN(network.STA_IF).active(False)
            ap = network.WLAN(network.AP_IF)
            client = network.WLAN(network.STA_IF)
        else:
            raise e
    return ap, client


ap, client = reset_wifi_mode()

app = Microdot()

CREDENTIALS_FILE = "wifi.conf"


def activateAP():
    if not ap.active():
        if client.active():
            print("Turning client off")
            client.active(0)
        print("Turning AP on", ap.ifconfig()[0])
        ap.active(1)
        return True
    else:
        return False


async def connectToWIFI(ssid, passw):
    if ap.active():
        print("Turning AP off")
        ap.active(False)
    if client.isconnected():
        print("Disconnecting from current wifi")
        client.disconnect()
    client.active(1)
    if not client.isconnected():
        try:
            client.config(dhcp_hostname="AWS")
            client.connect(ssid, passw)
        except Exception:
            client.active(False)
            return False
        n = 0
        print(f"Connecting to {ssid}", end="")
        while not client.isconnected():
            print(".", end="")
            await asyncio.sleep(1)
            n += 1
            if n == 60:
                break
        if n == 60:
            client.active(False)
            print("\nGiving up! Not connected!")
            raise ConnectionFailed
        else:
            print("\nNow connected with IP: ", client.ifconfig()[0])
            return True


@app.route("/")
async def index(request):
    print(f"Connection from {request.client_addr}")
    try:
        with open("web/setup.html", "r") as f:
            html_content = f.read()
    except IOError:
        print("Error: File not found or read error")
        html_content = "<h1>Error: File not found or read error</h1>"
    return html_content, {"Content-Type": "text/html"}


@app.route("/submit", methods=["POST"])
async def submit(request):
    ssid = request.form.get("ssid")
    password = request.form.get("password")
    email = request.form.get("email")
    asyncio.create_task(disconnectAndConnect(ssid, password))
    try:
        with open("web/success.html", "r") as f:
            html_content = f.read()
    except IOError:
        print("Error: File not found or read error")
        html_content = "<h1>Error: File not found or read error</h1>"
    save_credentials(ssid, password, email)
    return html_content, {"Content-Type": "text/html"}


class ConnectionFailed(Exception):
    pass


async def disconnectAndConnect(ssid, password):
    await asyncio.sleep(1)
    if client.isconnected():
        client.disconnect()
    try:
        await connectToWIFI(ssid, password)
    except ConnectionFailed:
        print("Failed to connect to new network. Turning on AP.")
        activateAP()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def save_credentials(ssid, password, email):
    with open(CREDENTIALS_FILE, "w") as f:
        f.write(f"{ssid}\n")
        f.write(f"{password}\n")
        f.write(f"{email}\n")


def load_wifi_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            ssid = f.readline().strip()
            password = f.readline().strip()
            return ssid, password
    except OSError:
        print("No wifi.conf file found.")
        return None, None


def load_email():
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            for i, line in enumerate(f):
                if i == 2:
                    email = line.strip()
                    break
            return email
    except OSError:
        print("No wifi.conf file found.")
        return None


sensor = Sensor()
alarm = Alarm(sensor)


def sendAlarm():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("79.171.148.171", 7913))
        message = str(load_email())
        s.sendall(message.encode())
        s.close()
    except Exception as e:
        print(f"Failed to send alarm: {e}")


async def read_sensor():
    run = 0
    while True:
        readings = sensor.read()
        # print(alarm.check(*readings), sensor.diff())
        if alarm.check(*readings):
            pass
        if not run:
            sendAlarm()
            run = 1
        await asyncio.sleep(1)


def run():
    try:
        ssid, password = load_wifi_credentials()
        if ssid and password:
            print("Trying to connect with saved credentials...")
            asyncio.run(disconnectAndConnect(ssid, password))
        else:
            activateAP()

        asyncio.create_task(read_sensor())
        app.run(port=80)
    except KeyboardInterrupt:
        print("\nStopped...")
    finally:
        ap.active(0)
        client.active(0)


if __name__ == "__main__":
    run()
