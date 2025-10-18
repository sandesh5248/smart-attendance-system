 Smart Attendance System

The **Smart Attendance System** is a simple and efficient web-based solution for managing and viewing attendance.  
This project uses **Python (Flask)** for the backend, **HTML** for the frontend, **Google Apps Script** for data handling, and **MIT App Inventor** for the mobile viewer app.


 1. Initialize Python and HTML Code on Raspberry Pi

a. Create the project folder  

   mkdir attendance
b.Create the Python file
Inside the attendance folder, create a new file named app.py.

c.Create the Templates folder
Inside the attendance folder, create a subfolder named templates.

d.Create the HTML file
Inside the templates folder, create a file named index.html.

e.Open Terminal and navigate to the folder

cd attendance
Run the Python application

python3 app.py
Copy the local server link displayed in the terminal (e.g., http://127.0.0.1:5000 or http://<raspberrypi_ip>:5000).

f.Paste the link into your browser.

 The web interface will load successfully.


 2. Initialize Google Apps Script (script.js)

    
a.Open Google Sheets or Google Drive.
b.Click on Extensions → Apps Script.
c.Paste your script.js code into the editor.
d.Click Deploy → New deployment.
e.Choose Web app as the deployment type.
f.Give a name to your project.
g.Under Access, select “Anyone”.
h.Click Deploy and grant the required permissions.
i.Copy the deployment URL to integrate with your web application.

3. Initialize Mobile App (attendance_viewer.aia)

   
a.Open MIT App Inventor.
b.Log in with your Google account.
c.Click Projects → Import project (.aia) from my computer.
d.Select and upload the attendance_viewer.aia file.
e.Click Build → App (provide QR code for .apk).
f.Scan the generated QR code using your mobile device to install the APK.
h.Open the installed mobile app.
i.Log in with the default credentials:
Username: admin
Password: 12345

j.The mobile app will display attendance data.


Project Structure

attendance/
├── app.py
├── templates/
│   └── index.html
└── README.md


Requirements
a.Raspberry Pi (or any system with Python 3)
b.Python 3 installed
c.Flask library (pip install flask)
d.Google Account (for Apps Script)
e.MIT App Inventor account
f.Web browser (Chrome, Firefox, etc.)
i.Internet connection

Default Login
Role	Username	Password
Admin	admin	12345

It is strongly recommended to change the default password after setup for security.

Notes

a.Make sure Raspberry Pi and your mobile device are connected to the same network.
b.Keep the Python server running to access the web interface and mobile app.
c.If you redeploy the Apps Script, update the deployment URL in your web or app code.
d.You can modify the MIT App Inventor .aia file to customize the mobile UI.

Author
Project: Smart Attendance System

Developed by: [Sandesh pokharkar]

Email: [sandeshpokharkar5248@gmail.com]
