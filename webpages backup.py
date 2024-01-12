wifi_config_page = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Wi-Fi Konfiguration</title>
    <style>
        body {font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;}
        .container {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); width: 300px;}
        h1 {color: #333; text-align: center;}
        form {display: flex; flex-direction: column; gap: 10px;}
        input[type=text], input[type=password] {padding: 10px; border-radius: 5px; border: 1px solid #ddd; font-size: 16px;}
        input[type=submit] {padding: 10px; border-radius: 5px; border: none; color: white; background-color: #007bff; cursor: pointer; font-size: 16px;}
        input[type=submit]:hover {background-color: #0056b3;}
    </style>
</head>
<body>
    <div class="container">
        <h1>Wi-Fi Konfiguration</h1>
        <form>
            SSID: <input type="text" name="ssid" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Forbind">
        </form>
    </div>
</body>
</html>
"""

login_page = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Login</title>
    <style>
        body {font-family: 'Arial', sans-serif; background-color: #e9ecef; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;}
        form {background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 300px;}
        h2 {text-align: center; margin-bottom: 20px;}
        input[type=text], input[type=password] {width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ced4da;}
        input[type=submit] {width: 100%; padding: 10px; border-radius: 5px; border: none; background-color: #007bff; color: white; cursor: pointer;}
        input[type=submit]:hover {background-color: #0056b3;}
    </style>
</head>
<body>
    <form>
        <h2>Login</h2>
        Brugernavn: <input type="text" name="username" required><br>
        Adgangskode: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

dashboard_page = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1, h2 {
            color: #343a40;
        }
        .dashboard-content, .email-form, .logout-form {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 20px;
            padding: 20px;
            width: 80%;
            max-width: 600px;
            text-align: center;
        }
        .data-table {
            margin: auto;
            border-collapse: collapse;
            width: 100%;
        }
        .data-table th, .data-table td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .data-table th {
            background-color: #007bff;
            color: white;
        }
        label {
            font-weight: bold;
        }
        input[type="email"], input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            border-radius: 4px;
            border: 1px solid #ced4da;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Dashboard</h1>
    <div class="dashboard-content">
        <h2>System Data</h2>
        <table class="data-table">
            <tr>
                <th>Data Type</th>
                <th>Value</th>
                <th>Unit</th>
            </tr>
            <tr>
                <td>Temperatur</td>
                <td>22.5</td>
                <td>°C</td>
            </tr>
            <tr>
                <td>Flowrate</td>
                <td>3.2</td>
                <td>L/min</td>
            </tr>
            <tr>
                <td>Vandtab Detekteret</td>
                <td>Nej</td>
                <td>-</td>
            </tr>
        </table>
    </div>
    <div class="email-form">
        <form method="post">
            <label for="email">Email til statusbeskeder:</label><br>
            <input type="email" id="email" name="email" required><br>
            <input type="submit" value="Gem Email">
        </form>
    </div>
    <div class="logout-form">
        <form action="/logout" method="post">
            <input type="submit" value="Log ud">
        </form>
    </div>
</body>
</html>
"""