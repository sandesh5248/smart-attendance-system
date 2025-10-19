# 🎯 Smart Attendance System  

A **smart and efficient web-based attendance management system** built using **Python (Flask)**, **HTML**, **Google Apps Script**, and **MIT App Inventor**.  
It allows easy attendance tracking, real-time syncing, and mobile viewing — ideal for schools, colleges, and offices.  

---

## 🚀 Features

- ✅ Simple and interactive **web interface**  
- ✅ **Automatic attendance marking** using ID cards  
- ✅ **Google Sheets integration** for storing attendance data  
- ✅ Cross-platform **mobile viewer app** (MIT App Inventor)  
- ✅ Secure **admin login** with credentials  
- ✅ Works seamlessly on **Raspberry Pi** or any local server  

---

## 🛠️ Tech Stack

| Component     | Technology Used                  |
|---------------|---------------------------------|
| Backend       | Python (Flask)                  |
| Frontend      | HTML, CSS                        |
| Database      | Google Sheets (via Apps Script) |
| Mobile App    | MIT App Inventor                 |
| Deployment    | Raspberry Pi / Localhost         |

---

## 📁 Project Structure

attendance/
├── app.py
├── templates/
│ └── index.html
└── README.md




## ⚙️ Setup Instructions<br><br>

### 1️⃣ Create the Project

# Create project folder
mkdir attendance

# Move inside the folder
cd attendance
Create the following:

app.py → main Flask app

templates/index.html → frontend web UI<br><br>

2️⃣ Run the Application
bash
Copy code
python3 app.py
Open your browser and visit:

🔗 http://127.0.0.1:5000

🔗 http://<raspberrypi_ip>:5000

✅ The web interface will load successfully.<br><br>

3️⃣ Google Apps Script (script.js)
Open Google Sheets → Extensions → Apps Script

Paste your script.js code

Click Deploy → New deployment

Choose Web app as the type

Set Access → Anyone and click Deploy

Copy the Deployment URL to integrate with your web app<br><br>

4️⃣ MIT App (attendance_viewer.aia)
Open MIT App Inventor → https://appinventor.mit.edu

Click Projects → Import Project (.aia)

Upload attendance_viewer.aia

Go to Build → App (.apk) and scan the generated QR Code

Install and open the app

Login using:

Role	Username	Password
Admin	admin	12345

✅ The mobile app will show real-time attendance data.<br><br>

🧩 Requirements<br>
Python 3

Flask → pip install flask

Google Account (for Apps Script)

MIT App Inventor Account

Internet Connection

Web Browser (Chrome / Firefox)<br><br>

💾 Excel Sheet Integration<br><br>

📊 The system uses Google Sheets as the backend database.

Your Excel Sheet (Google Sheet) acts as both input and output for attendance data.

Each scan (via card or ID) automatically updates the sheet

Admin can view or edit data directly from the connected sheet

🔗 Example Integration:
https://docs.google.com/spreadsheets/d/<your_sheet_id>/edit?usp=sharing


🎨 UI Design<br><br>
💳 Scanning & Attendance Marking<br>
Modern, minimal web interface for scanning ID cards. Each successful scan marks attendance and syncs instantly with Google Sheets. Responsive layout suitable for PCs, tablets, and Raspberry Pi touchscreens.

Action	Description<br>
Scan Card	Reads ID via card reader and verifies identity
Mark Attendance	Automatically updates the connected Excel sheet
Status Display	Shows “Present” / “Already Marked” instantly
Admin Access	Allows viewing, editing, and exporting data

<img width="754" height="510" alt="Scanning Interface" src="https://github.com/user-attachments/assets/bae6354e-8961-410e-976e-53a46a3f18a0" /><br><br>

🧾 Excel Sheet Link (Input & Output)
All attendance data is synced here.

✅ Automatically updates every scan

✅ Accessible to admin and teachers

✅ Supports timestamp and name-based logging

<img width="600" height="596" alt="Excel Sheet Output" src="https://github.com/user-attachments/assets/ac78a5ef-b2c3-4c94-9ccb-4375ca97f9f7" /><br><br>

📱 MIT App Output

🖥️ Screen 1 – Login Screen

Login Screen – secure admin access<br>

<img width="358" height="519" alt="Login Screen" src="https://github.com/user-attachments/assets/f70762f8-6420-4ffa-bc48-fbc601a2019b" /><br><br>

📋 Screen 2 – Dashboard

Dashboard – quick view of attendance summary

<img width="362" height="508" alt="Dashboard Screen" src="https://github.com/user-attachments/assets/901ba51a-6066-4879-b2d8-70c201d91a6b" /><br><br>

👥 Screen 3 – Attendance List : Student-wise

<img width="368" height="546" alt="Student Attendance" src="https://github.com/user-attachments/assets/3eceb024-809e-456c-af27-34ec8c793f30" /><br><br>

⚙️ Screen 4 – Lecture-wise Attendance<br>
<img width="366" height="550" alt="Lecture Attendance" src="https://github.com/user-attachments/assets/48f60bdc-527a-4b56-9daa-8f35586e3343" /><br><br>
⚠️ Security Notes<br>
🔒 Always change the default password (admin / 12345) after installation<br>
🔒 Use private Google Sheets links for better data safety<br><br>

👨‍💻 Developer Info<br>
Project: Smart Attendance System<br>
Developed by: Sandesh Pokharkar<br>
Email: sandeshpokharkar5248@gmail.com<br>

Preview<br>
🎨 Clean, responsive web UI for attendance management<br>
📱 Mobile viewer app synced in real-time with Google Sheets<br>
