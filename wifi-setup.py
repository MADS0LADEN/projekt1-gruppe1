import network
import socket
from time import sleep
import webpages  # Importér HTML-siderne

# Opsætning af ESP32 som et access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='Wifi-setup', password='123456789')

# Få AP's IP-adresse
ap_ip = ap.ifconfig()[0]
print('Access Point aktivt.')
print('Access Point IP: ', ap_ip)

# Definer WLAN-interface for klientforbindelse
wifi = network.WLAN(network.STA_IF)
wifi.active(False)  # Sørg for, at Wi-Fi klienten ikke er aktiv til at starte med

# Definer testbrugere og email-adresse
brugere = {
    "admin1": "password1",
    "admin2": "password2"
}
email_address = ""

er_logget_ind = False

# Opret en socket til at hoste webserveren
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

while True:
    cl = None
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)
        request = str(request)

        if 'ssid=' in request and 'password=' in request:
            ssid_start = request.find('ssid=') + 5
            ssid_end = request.find('&', ssid_start)
            password_start = request.find('password=') + 9
            password_end = request.find(' ', password_start)

            ssid = request[ssid_start:ssid_end]
            password = request[password_start:password_end]

            ap.active(False)
            wifi.active(True)
            wifi.connect(ssid, password)

            while not wifi.isconnected():
                pass

            print('Forbundet til:', ssid)
            print('IP-adresse:', wifi.ifconfig()[0])

            response = """<!DOCTYPE html>
            <html>
            <body>
                <h2>Forbinder til Wi-Fi...</h2>
                <p>Vent venligst mens forbindelsen til {} etableres.</p>
                <p>Genbesøg siden på IP: <a href="http://{}">{}</a> efter nogle sekunder.</p>
            </body>
            </html>
            """.format(ssid, wifi.ifconfig()[0], wifi.ifconfig()[0])
        elif wifi.isconnected():
            if 'username=' in request and 'password=' in request:
                username_start = request.find('username=') + 9
                username_end = request.find('&', username_start)
                password_start = request.find('password=') + 9
                password_end = request.find(' ', password_start)
                username = request[username_start:username_end]
                password = request[password_start:password_end]

                if username in brugere and brugere[username] == password:
                    er_logget_ind = True  # Sæt til true ved succesfuldt login
                    response = webpages.dashboard_page
                else:
                    response = webpages.login_page
            elif '/logout' in request:
                er_logget_ind = False  # Nulstil ved log ud
                response = webpages.login_page
            elif er_logget_ind:
                response = webpages.dashboard_page  # Vis kun dashboard, hvis logget ind
            else:
                response = webpages.login_page  # Ellers vis login-siden
        else:
            response = webpages.wifi_config_page

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSError as e:
        if cl:
            cl.close()

s.close()
