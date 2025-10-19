<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Attendance System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f9f9f9;
            color: #333;
        }
        h1, h2, h3, h4 {
            color: #2c3e50;
        }
        h1 {
            text-align: center;
        }
        code {
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 4px;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
        table, th, td {
            border: 1px solid #aaa;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        img {
            max-width: 100%;
            margin: 10px 0;
            border-radius: 5px;
        }
        .section {
            background-color: #fff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 0 8px rgba(0,0,0,0.05);
        }
        a {
            color: #2980b9;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .command {
            background-color: #2c3e50;
            color: #fff;
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px 0;
        }
        ul {
            margin: 10px 0;
        }
        .center {
            text-align: center;
        }
    </style>
</head>
<body>

    <h1>🎯 Smart Attendance System</h1>

    <div class="section">
        <p>
            A <strong>smart and efficient web-based attendance management system</strong> built using 
            <strong>Python (Flask)</strong>, <strong>HTML</strong>, <strong>Google Apps Script</strong>, and 
            <strong>MIT App Inventor</strong>. It allows easy attendance tracking, real-time syncing, 
            and mobile viewing — ideal for schools, colleges, and offices.
        </p>
    </div>

    <div class="section">
        <h2>🚀 Features</h2>
        <ul>
            <li>✅ Simple and interactive <strong>web interface</strong></li>
            <li>✅ <strong>Automatic attendance marking</strong> using ID cards</li>
            <li>✅ <strong>Google Sheets integration</strong> for storing attendance data</li>
            <li>✅ Cross-platform <strong>mobile viewer app</strong> (MIT App Inventor)</li>
            <li>✅ Secure <strong>admin login</strong> with credentials</li>
            <li>✅ Works seamlessly on <strong>Raspberry Pi</strong> or any local server</li>
        </ul>
    </div>

    <div class="section">
        <h2>🛠️ Tech Stack</h2>
        <table>
            <tr>
                <th>Component</th>
                <th>Technology Used</th>
            </tr>
            <tr>
                <td>Backend</td>
                <td>Python (Flask)</td>
            </tr>
            <tr>
                <td>Frontend</td>
                <td>HTML, CSS</td>
            </tr>
            <tr>
                <td>Database</td>
                <td>Google Sheets (via Apps Script)</td>
            </tr>
            <tr>
                <td>Mobile App</td>
                <td>MIT App Inventor</td>
            </tr>
            <tr>
                <td>Deployment</td>
                <td>Raspberry Pi / Localhost</td>
            </tr>
        </table>
    </div>

    <div class="section">
        <h2>📁 Project Structure</h2>
        <pre>
attendance/
├── app.py
├── templates/
│   └── index.html
└── README.md
        </pre>
    </div>

    <div class="section">
        <h2>⚙️ Setup Instructions</h2>
        <h3>1️⃣ Create the Project</h3>
        <pre>
# Create project folder
mkdir attendance

# Move inside the folder
cd attendance

# Create files
app.py → main Flask app
templates/index.html → frontend web UI
        </pre>

        <h3>2️⃣ Run the Application</h3>
        <pre>
python3 app.py
        </pre>
        <p>Open your browser and visit:</p>
        <ul>
            <li>🔗 <a href="http://127.0.0.1:5000" target="_blank">http://127.0.0.1:5000</a></li>
            <li>🔗 http://&lt;raspberrypi_ip&gt;:5000</li>
        </ul>
        <p>✅ The web interface will load successfully.</p>

        <h3>3️⃣ Google Apps Script (script.js)</h3>
        <ul>
            <li>Open Google Sheets → Extensions → Apps Script</li>
            <li>Paste your script.js code</li>
            <li>Click Deploy → New deployment</li>
            <li>Choose Web app as the type</li>
            <li>Set Access → Anyone and click Deploy</li>
            <li>Copy the Deployment URL to integrate with your web app</li>
        </ul>

        <h3>4️⃣ MIT App (attendance_viewer.aia)</h3>
        <ul>
            <li>Open MIT App Inventor → <a href="https://appinventor.mit.edu" target="_blank">https://appinventor.mit.edu</a></li>
            <li>Click Projects → Import Project (.aia)</li>
            <li>Upload attendance_viewer.aia</li>
            <li>Go to Build → App (.apk) and scan the QR Code</li>
            <li>Install and open the app</li>
            <li>Login using:</li>
        </ul>
        <table>
            <tr><th>Role</th><th>Username</th><th>Password</th></tr>
            <tr><td>Admin</td><td>admin</td><td>12345</td></tr>
        </table>
        <p>✅ The mobile app will show real-time attendance data.</p>
    </div>

    <div class="section">
        <h2>🧩 Requirements</h2>
        <ul>
            <li>Python 3</li>
            <li>Flask → <code>pip install flask</code></li>
            <li>Google Account (for Apps Script)</li>
            <li>MIT App Inventor Account</li>
            <li>Internet Connection</li>
            <li>Web Browser (Chrome / Firefox)</li>
        </ul>
    </div>

    <div class="section">
        <h2>💾 Excel Sheet Integration</h2>
        <p>📊 The system uses <strong>Google Sheets</strong> as the backend database.  
        Your Excel Sheet acts as both input and output for attendance data.</p>
        <ul>
            <li>Each scan (via card or ID) automatically updates the sheet</li>
            <li>Admin can view or edit data directly from the connected sheet</li>
        </ul>
        <p>🔗 Example Integration:</p>
        <pre>https://docs.google.com/spreadsheets/d/&lt;your_sheet_id&gt;/edit?usp=sharing</pre>
    </div>

    <div class="section">
        <h2>🎨 UI Design</h2>
        <h3>💳 Scanning & Attendance Marking</h3>
        <ul>
            <li>Modern, minimal web interface for scanning ID cards</li>
            <li>Each successful scan marks attendance and syncs instantly with Google Sheets</li>
            <li>Responsive layout suitable for PCs, tablets, and Raspberry Pi touchscreens</li>
        </ul>
        <table>
            <tr><th>Action</th><th>Description</th></tr>
            <tr><td>Scan Card</td><td>Reads ID via card reader and verifies identity</td></tr>
            <tr><td>Mark Attendance</td><td>Automatically updates the connected Excel sheet</td></tr>
            <tr><td>Status Display</td><td>Shows “Present” / “Already Marked” instantly</td></tr>
            <tr><td>Admin Access</td><td>Allows viewing, editing, and exporting data</td></tr>
        </table>

        <div class="center">
            <img src="https://github.com/user-attachments/assets/bae6354e-8961-410e-976e-53a46a3f18a0" alt="Scanning Interface">
        </div>
    </div>

    <div class="section">
        <h2>🧾 Excel Sheet Link (Input & Output)</h2>
        <p>All attendance data is synced here.</p>
        <ul>
            <li>✅ Automatically updates every scan</li>
            <li>✅ Accessible to admin and teachers</li>
            <li>✅ Supports timestamp and name-based logging</li>
        </ul>
        <div class="center">
            <img src="https://github.com/user-attachments/assets/ac78a5ef-b2c3-4c94-9ccb-4375ca97f9f7" alt="Excel Sheet Output">
        </div>
    </div>

    <div class="section">
        <h2>📱 MIT App Output</h2>
        <h3>🖥️ Screen 1 – Login Screen</h3>
        <div class="center">
            <img src="https://github.com/user-attachments/assets/f70762f8-6420-4ffa-bc48-fbc601a2019b" alt="Login Screen">
        </div>

        <h3>📋 Screen 2 – Dashboard</h3>
        <div class="center">
            <img src="https://github.com/user-attachments/assets/901ba51a-6066-4879-b2d8-70c201d91a6b" alt="Dashboard Screen">
        </div>

        <h3>👥 Screen 3 – Attendance List</h3>
        <div class="center">
            <img src="https://github.com/user-attachments/assets/3eceb024-809e-456c-af27-34ec8c793f30" alt="Student Attendance">
        </div>

        <h3>⚙️ Screen 4 – Lecture-wise Attendance</h3>
        <div class="center">
            <img src="https://github.com/user-attachments/assets/48f60bdc-527a-4b56-9daa-8f35586e3343" alt="Lecture Attendance">
        </div>
    </div>

    <div class="section">
        <h2>⚠️ Security Notes</h2>
        <ul>
            <li>🔒 Always change the default password (<code>admin / 12345</code>) after installation</li>
            <li>🔒 Use private Google Sheets links for better data safety</li>
        </ul>
    </div>

    <div class="section">
        <h2>👨‍💻 Developer Info</h2>
        <p>
            <strong>Project:</strong> Smart Attendance System<br>
            <strong>Developed by:</strong> Sandesh Pokharkar<br>
            <strong>Email:</strong> <a href="mailto:sandeshpokharkar5248@gmail.com">sandeshpokharkar5248@gmail.com</a>
        </p>
    </div>

    <div class="section">
        <h2>🖥️ Preview</h2>
        <ul>
            <li>🎨 Clean, responsive web UI for attendance management</li>
            <li>📱 Mobile viewer app synced in real-time with Google Sheets</li>
        </ul>
    </div>

</body>
</html>
