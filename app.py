from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, time
import time as time_module
import requests
import serial
import threading
import serial.tools.list_ports

app = Flask(__name__)

# ---------------- CONFIG ----------------
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx8LK-Caj0IVcoP4hEeBK3lcitvLX67vx9s4BVef2QVcHN9gIxY6xHQDrbm0PdpdAERZQ/exec"

# RFID Configuration - Auto-detect or manual
RFID_BAUD_RATE = 9600
rfid_serial = None
rfid_connected = False

REGISTERED_USERS = {}
attendance_enabled = False
current_teacher_subject = None
current_teacher_card = None
last_scanned_card = None
card_scan_callback = None

# Lecture timings (24-hour format)
LECTURE_SLOTS = {
    1: {"start": time(19, 0), "end": time(20, 0)},
    2: {"start": time(10, 30), "end": time(12, 30)},
    3: {"start": time(13, 0), "end": time(15, 0)},
    4: {"start": time(15, 45), "end": time(17, 0)}
}

# ---------------- RFID FUNCTIONS ----------------

def detect_serial_ports():
    """Detect available serial ports"""
    ports = []
    try:
        available_ports = serial.tools.list_ports.comports()
        for port in available_ports:
            ports.append({
                'device': port.device,
                'description': port.description,
                'hwid': port.hwid
            })
            print(f"🔍 Found port: {port.device} - {port.description}")
    except Exception as e:
        print(f"❌ Error detecting ports: {e}")
    return ports

def setup_rfid_reader():
    """Initialize RFID reader with auto-detection"""
    global rfid_serial, rfid_connected

    # Try to auto-detect RFID reader
    ports = detect_serial_ports()
    target_port = None

    # Common RFID reader descriptions
    rfid_keywords = ['usb', 'serial', 'uart', 'ch340', 'cp210', 'ftdi', 'em-18', 'rfid']

    for port in ports:
        description_lower = port['description'].lower()
        if any(keyword in description_lower for keyword in rfid_keywords):
            target_port = port['device']
            print(f"🎯 Potential RFID reader found: {port['device']} - {port['description']}")
            break

    # If no auto-detection, try common ports
    common_ports = ['COM3', 'COM4', 'COM5', 'COM6', '/dev/ttyUSB0', '/dev/ttyACM0', '/dev/tty.usbserial']

    for port in common_ports:
        if not target_port:  # Only try if no target from auto-detection
            try:
                test_ser = serial.Serial(port, RFID_BAUD_RATE, timeout=1)
                test_ser.close()
                target_port = port
                print(f"✅ Port {port} is available")
                break
            except:
                print(f"❌ Port {port} not available")
                continue

    if not target_port:
        print("❌ No suitable serial port found for RFID reader")
        return None

    try:
        rfid_serial = serial.Serial(
            port=target_port,
            baudrate=RFID_BAUD_RATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1  # Short timeout for responsive reading
        )
        rfid_connected = True
        print(f"✅ RFID Reader connected on {target_port}")
        return rfid_serial
    except Exception as e:
        print(f"❌ Failed to connect to RFID reader on {target_port}: {e}")
        rfid_connected = False
        return None

def read_rfid_card(ser):
    """Read RFID card from serial port with improved parsing"""
    if not ser:
        return None

    try:
        if ser.in_waiting > 0:
            # Read all available data
            data = ser.readline().decode('utf-8', errors='ignore').strip()

            # EM-18 typically sends 12-character IDs (sometimes with \r\n)
            if len(data) >= 10:  # Allow for some variations
                # Extract only alphanumeric characters (remove any control characters)
                clean_data = ''.join(char for char in data if char.isalnum())

                if len(clean_data) >= 10:  # Valid RFID card ID
                    print(f"📖 Raw RFID data: '{data}' -> Clean: '{clean_data}'")
                    return clean_data
                else:
                    print(f"📖 Invalid RFID data: '{data}'")

        return None
    except Exception as e:
        print(f"❌ Error reading RFID: {e}")
        return None

def simulate_rfid_reader():
    """Simulate RFID reader for testing without hardware"""
    print("🎮 Using simulated RFID reader for testing")
    simulated_cards = [
        "123456789012",
        "234567890123",
        "345678901234",
        "456789012345",
        "567890123456"
    ]
    card_index = 0

    while True:
        # Simulate card scan every 10 seconds for testing
        time_module.sleep(10)

        global last_scanned_card
        simulated_card = simulated_cards[card_index]
        last_scanned_card = simulated_card
        print(f"🎫 Simulated card scan: {simulated_card}")

        # Call callback function if set
        if card_scan_callback:
            card_scan_callback(simulated_card)

        card_index = (card_index + 1) % len(simulated_cards)

def rfid_reading_thread():
    """Background thread for continuous RFID reading"""
    global rfid_connected

    print("🔄 Starting RFID reader thread...")

    # Try to setup real RFID reader
    ser = setup_rfid_reader()

    if not ser:
        print("❌ No RFID hardware found. Using simulation mode.")
        rfid_connected = False
        simulate_rfid_reader()
        return

    rfid_connected = True
    last_card = None
    last_read_time = 0
    debounce_time = 2  # seconds between same card reads

    print("✅ RFID reader thread started successfully")

    while True:
        try:
            card_id = read_rfid_card(ser)
            current_time = time_module.time()

            if card_id and card_id != last_card or (current_time - last_read_time) > debounce_time:
                last_card = card_id
                last_read_time = current_time

                print(f"🎫 Card scanned: {card_id}")

                # Store the scanned card globally
                global last_scanned_card
                last_scanned_card = card_id

                # Call callback function if set
                if card_scan_callback:
                    card_scan_callback(card_id)

        except Exception as e:
            print(f"❌ RFID thread error: {e}")
            # Try to reconnect
            try:
                ser.close()
            except:
                pass
            time_module.sleep(5)
            ser = setup_rfid_reader()

        time_module.sleep(0.1)  # Small delay to prevent excessive CPU usage

# ---------------- EXISTING FUNCTIONS ----------------

def get_lecture_slot():
    """Get current lecture slot based on time"""
    now = datetime.now().time()
    for slot_num, slot_info in LECTURE_SLOTS.items():
        if slot_info["start"] <= now <= slot_info["end"]:
            return slot_num
    return None

def get_student_status():
    """Determine if student is On-time or Late"""
    now = datetime.now()
    current_slot = get_lecture_slot()
    if not current_slot:
        return "Invalid Time"

    slot_start = LECTURE_SLOTS[current_slot]["start"]
    grace_end_minutes = slot_start.minute + 15
    grace_end_hours = slot_start.hour
    if grace_end_minutes >= 60:
        grace_end_hours += 1
        grace_end_minutes -= 60
    grace_period_end = time(grace_end_hours, grace_end_minutes)

    if slot_start <= now.time() <= grace_period_end:
        return "On-time"
    else:
        return "Late"

def send_to_google_sheet(role, data, register_only=False):
    payload = data.copy()
    payload["role"] = role
    if register_only:
        payload["register_only"] = True

    try:
        response = requests.post(WEB_APP_URL, data=json.dumps(payload))
        if response.status_code == 200:
            print("✅ Data sent successfully!")
            return True
        else:
            print(f"❌ Failed to send data ({response.status_code})")
            return False
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return False

def preload_registered_users():
    global REGISTERED_USERS
    try:
        response = requests.get(WEB_APP_URL + "?tab=Register", timeout=10)
        if response.status_code != 200:
            print("❌ Failed to fetch registered users")
            return
        users = response.json()
        REGISTERED_USERS = {
            str(u["card_id"]): {
                "role": u["role"].lower(),
                "name": u["name"],
                "roll_no": u.get("roll_no", "-"),
                "subject": u.get("subject", "-")
            }
            for u in users
        }
        print(f"✅ Loaded {len(REGISTERED_USERS)} registered users")
    except Exception as e:
        print(f"⚠️ Error fetching users: {e}")

# ---------------- FLASK ROUTES ----------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_rfid_status', methods=['GET'])
def get_rfid_status():
    """Get RFID reader connection status"""
    global rfid_connected
    ports = detect_serial_ports()
    return jsonify({
        'rfid_connected': rfid_connected,
        'available_ports': ports
    })

@app.route('/manual_port', methods=['POST'])
def set_manual_port():
    """Set manual serial port"""
    global rfid_serial, rfid_connected

    data = request.json
    port = data.get('port')

    if not port:
        return jsonify({'success': False, 'message': 'No port specified'})

    try:
        if rfid_serial:
            rfid_serial.close()

        rfid_serial = serial.Serial(
            port=port,
            baudrate=RFID_BAUD_RATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1
        )
        rfid_connected = True
        return jsonify({'success': True, 'message': f'Connected to {port}'})
    except Exception as e:
        rfid_connected = False
        return jsonify({'success': False, 'message': f'Failed to connect: {str(e)}'})

# ... (keep all the existing routes from previous code - they remain the same)

@app.route('/load_users', methods=['POST'])
def load_users():
    try:
        preload_registered_users()
        return jsonify({
            'success': True,
            'message': f'Loaded {len(REGISTERED_USERS)} registered users',
            'user_count': len(REGISTERED_USERS)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading users: {str(e)}'
        })

@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        data = request.json
        card_id = data.get('card_id')
        name = data.get('name')
        role = data.get('role')
        roll_no = data.get('roll_no', '-')
        subject = data.get('subject', '-')

        if not all([card_id, name, role]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            })

        success = send_to_google_sheet(role, {
            "card_id": card_id,
            "role": role,
            "name": name,
            "roll_no": roll_no,
            "subject": subject,
            "date": datetime.now().strftime("%Y-%m-%d")
        }, register_only=True)

        if success:
            REGISTERED_USERS[card_id] = {
                "role": role,
                "name": name,
                "roll_no": roll_no,
                "subject": subject
            }
            return jsonify({
                'success': True,
                'message': 'User registered successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Registration failed!'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/start_attendance', methods=['POST'])
def start_attendance():
    global attendance_enabled, current_teacher_subject, current_teacher_card

    try:
        if not REGISTERED_USERS:
            return jsonify({
                'success': False,
                'message': 'No registered users found. Please load users first.'
            })

        current_slot = get_lecture_slot()
        if not current_slot:
            return jsonify({
                'success': False,
                'message': 'No active lecture session'
            })

        data = request.json
        teacher_card = data.get('card_id')

        teacher_user = REGISTERED_USERS.get(teacher_card)
        if not teacher_user or teacher_user["role"] != "teacher":
            return jsonify({
                'success': False,
                'message': 'Invalid teacher card'
            })

        now = datetime.now()
        send_to_google_sheet("teacher", {
            "card_id": teacher_card,
            "name": teacher_user["name"],
            "subject": teacher_user["subject"],
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "status": f"Lecture Started - Slot {current_slot}",
            "lecture_slot": current_slot
        })

        current_teacher_subject = teacher_user["subject"]
        current_teacher_card = teacher_card
        attendance_enabled = True

        return jsonify({
            'success': True,
            'message': f'Lecture started! Subject: {current_teacher_subject}',
            'subject': current_teacher_subject,
            'lecture_slot': current_slot
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    global attendance_enabled, current_teacher_subject, current_teacher_card

    try:
        if not attendance_enabled:
            return jsonify({
                'success': False,
                'message': 'Attendance session not started'
            })

        data = request.json
        card_id = data.get('card_id')

        # Handle force end
        if card_id == 'FORCE_END' and attendance_enabled:
            current_slot = get_lecture_slot()
            if current_teacher_card:
                teacher_user = REGISTERED_USERS.get(current_teacher_card)
                if teacher_user:
                    send_to_google_sheet("teacher", {
                        "card_id": current_teacher_card,
                        "name": teacher_user["name"],
                        "subject": teacher_user["subject"],
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Lecture Ended (Forced)",
                        "lecture_slot": current_slot
                    })

            attendance_enabled = False
            current_teacher_subject = None
            current_teacher_card = None

            return jsonify({
                'success': True,
                'message': 'Lecture ended successfully',
                'action': 'end_lecture'
            })

        if card_id == current_teacher_card:
            # End lecture
            current_slot = get_lecture_slot()
            teacher_user = REGISTERED_USERS.get(card_id)
            send_to_google_sheet("teacher", {
                "card_id": card_id,
                "name": teacher_user["name"],
                "subject": teacher_user["subject"],
                "time": datetime.now().strftime("%H:%M:%S"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Lecture Ended",
                "lecture_slot": current_slot
            })
            attendance_enabled = False
            current_teacher_subject = None
            current_teacher_card = None

            return jsonify({
                'success': True,
                'message': 'Lecture ended successfully',
                'action': 'end_lecture'
            })

        user = REGISTERED_USERS.get(card_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Card not registered'
            })

        role = user["role"]
        now = datetime.now()
        date_today = now.strftime("%Y-%m-%d")
        time_now = now.strftime("%H:%M:%S")
        current_slot = get_lecture_slot()

        if role == "student":
            status = get_student_status()
            success = send_to_google_sheet("student", {
                "card_id": card_id,
                "name": user["name"],
                "roll_no": user["roll_no"],
                "subject": current_teacher_subject,
                "time": time_now,
                "date": date_today,
                "status": status,
                "lecture_slot": current_slot
            })

            if success:
                return jsonify({
                    'success': True,
                    'message': f'Attendance marked: {user["name"]} - {status}',
                    'name': user['name'],
                    'status': status,
                    'role': 'student'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to send attendance data'
                })

        elif role == "teacher":
            return jsonify({
                'success': True,
                'message': f'Teacher attendance: {user["name"]}',
                'name': user['name'],
                'role': 'teacher'
            })

        elif role == "admin":
            return jsonify({
                'success': True,
                'message': f'Admin attendance: {user["name"]}',
                'name': user['name'],
                'role': 'admin'
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/force_end_lecture', methods=['POST'])
def force_end_lecture():
    global attendance_enabled, current_teacher_subject, current_teacher_card

    try:
        if not attendance_enabled:
            return jsonify({
                'success': False,
                'message': 'No active lecture session'
            })

        # Get current session info
        current_slot = get_lecture_slot()

        if current_teacher_card:
            teacher_user = REGISTERED_USERS.get(current_teacher_card)
            if teacher_user:
                send_to_google_sheet("teacher", {
                    "card_id": current_teacher_card,
                    "name": teacher_user["name"],
                    "subject": teacher_user["subject"],
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Lecture Ended (Forced)",
                    "lecture_slot": current_slot
                })

        # Reset session variables
        attendance_enabled = False
        current_teacher_subject = None
        current_teacher_card = None

        return jsonify({
            'success': True,
            'message': 'Lecture ended successfully'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/get_current_session', methods=['GET'])
def get_current_session():
    return jsonify({
        'attendance_enabled': attendance_enabled,
        'current_subject': current_teacher_subject,
        'current_lecture_slot': get_lecture_slot()
    })

@app.route('/get_scanned_card', methods=['GET'])
def get_scanned_card():
    """Get the last scanned card ID"""
    global last_scanned_card
    card = last_scanned_card
    last_scanned_card = None  # Clear after reading
    return jsonify({'card_id': card})

@app.route('/set_scan_mode', methods=['POST'])
def set_scan_mode():
    """Set the current scanning mode"""
    global card_scan_callback

    data = request.json
    mode = data.get('mode')

    if mode == 'registration':
        card_scan_callback = handle_registration_scan
    elif mode == 'attendance':
        card_scan_callback = handle_attendance_scan
    elif mode == 'start_attendance':
        card_scan_callback = handle_start_attendance_scan
    else:
        card_scan_callback = None

    return jsonify({'success': True, 'message': f'Scan mode set to: {mode}'})

def handle_registration_scan(card_id):
    """Handle card scan for registration mode"""
    print(f"📝 Registration scan: {card_id}")

def handle_attendance_scan(card_id):
    """Handle card scan for attendance mode"""
    print(f"📋 Attendance scan: {card_id}")

def handle_start_attendance_scan(card_id):
    """Handle card scan for starting attendance"""
    print(f"🎯 Start attendance scan: {card_id}")

if __name__ == '__main__':
    print("🏫 RFID ATTENDANCE SYSTEM READY")
    print("Loading registered users...")
    preload_registered_users()

    # Start RFID reading thread
    print("Starting RFID reader...")
    rfid_thread = threading.Thread(target=rfid_reading_thread, daemon=True)
    rfid_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5001)

