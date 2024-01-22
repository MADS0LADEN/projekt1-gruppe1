import asyncio

import network
from microdot import Microdot
from sensor import *

ap = network.WLAN(network.AP_IF)
mac = "".join(["%02x" % b for b in ap.config("mac")])
ap.config(ssid=f"Lækagealarm-{mac[-4:]}")
ap.config(max_clients=1)

client = network.WLAN(network.STA_IF)

app = Microdot()

CREDENTIALS_FILE = "wifi.txt"


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
        client.disconnect()  # Disconnect from the current network
    try:
        await connectToWIFI(ssid, password)
    except ConnectionFailed:
        print("Failed to connect to new network. Turning on AP.")
        activateAP()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def save_credentials(ssid, password, email):
    with open(CREDENTIALS_FILE, "w") as f:
        f.write(f"SSID: {ssid}\n")
        f.write(f"Password: {password}\n")
        f.write(f"Email: {email}\n")


def run():
    try:
        activateAP()
        app.run(port=80)
    except KeyboardInterrupt:
        print("Stopped...")
    finally:
        ap.active(0)
        client.active(0)
        app.shutdown()


if __name__ == "__main__":
    run()
