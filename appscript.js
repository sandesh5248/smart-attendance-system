function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const params = JSON.parse(e.postData.contents);
    const role = (params.role || "").toLowerCase();

    // ✅ Handle registration requests
    if (params.register_only === true) {
      let registerSheet = ss.getSheetByName("Register");
      if (!registerSheet) {
        registerSheet = ss.insertSheet("Register");
        registerSheet.appendRow(["card_id", "role", "name", "roll_no", "subject", "date"]);
      }

      registerSheet.appendRow([
        params.card_id || "-",
        params.role || "-",
        params.name || "-",
        params.roll_no || "-",
        params.subject || "-",
        params.date || new Date()
      ]);

      return jsonResponse({ success: true, message: "User registered successfully!" });
    }

    // ✅ Handle attendance logging based on role
    let sheetName = "";
    let headers = [];

    if (role === "student") {
      sheetName = "Student";
      headers = ["card_id", "name", "roll_no", "subject", "time", "date", "status", "role"];
    } else if (role === "teacher") {
      sheetName = "Teacher";
      headers = ["card_id", "name", "subject", "time", "date", "status", "role"];
    } else if (role === "admin") {
      sheetName = "Admin";
      headers = ["card_id", "name", "time", "date", "status", "role"];
    } else {
      return jsonResponse({ success: false, message: "Invalid or missing role!" });
    }

    let sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
      sheet.appendRow(headers);
    }

    const row = [
      params.card_id || "-",
      params.name || "-",
    ];

    if (role === "student") {
      row.push(
        params.roll_no || "-",
        params.subject || "-",
        params.time || new Date().toLocaleTimeString(),
        params.date || new Date().toLocaleDateString(),
        params.status || "Present",
        "Student"
      );
    } else if (role === "teacher") {
      row.push(
        params.subject || "-",
        params.time || new Date().toLocaleTimeString(),
        params.date || new Date().toLocaleDateString(),
        params.status || "Present",
        "Teacher"
      );
    } else if (role === "admin") {
      row.push(
        params.time || new Date().toLocaleTimeString(),
        params.date || new Date().toLocaleDateString(),
        params.status || "Active",
        "Admin"
      );
    }

    sheet.appendRow(row);

    return jsonResponse({ success: true, message: "Attendance recorded!" });
  } catch (error) {
    return jsonResponse({ success: false, error: error.toString() });
  }
}

function doGet(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const tab = e.parameter.tab;
    const sheet = ss.getSheetByName(tab);

    if (!sheet) {
      return jsonResponse({ error: "Sheet not found!" });
    }

    const data = sheet.getDataRange().getDisplayValues(); // ← FIXED: Use getDisplayValues()
    const headers = data[0];
    const rows = data.slice(1);
    
    const json = rows.map(row => {
      let obj = {};
      headers.forEach((header, index) => {
        obj[header] = row[index];
      });
      return obj;
    });

    return jsonResponse(json);
  } catch (error) {
    return jsonResponse({ error: error.toString() });
  }
}

// ✅ Helper: Standardized JSON response
function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
