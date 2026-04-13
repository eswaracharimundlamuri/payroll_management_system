#  Payroll Management System (GUI)

A Python-based **Payroll Management System** with a graphical user interface built using **Tkinter**.
This application calculates employee salaries using backend data sources like Oracle DB and AWS S3.

---

##  Project Overview

This system allows users to:

* Enter an employee name
* Fetch employee details from backend
* Automatically calculate salary components
* Display complete salary breakdown in GUI

---

##  Features

* User-friendly GUI using Tkinter
* Salary breakdown calculation:

  * Basic Salary
  * HRA (House Rent Allowance)
  * DA (Dearness Allowance)
  * Special Allowance
  * Gross Salary
  * PF (Provident Fund)
  * Tax & Cess
  * Net Salary
  *  Reset functionality
  *  Exit option
  * Error handling with popups

---

##  System Architecture

```
GUI (Tkinter)
   ↓
PayrollGUI (Frontend Logic)
   ↓
PayrollManagementSystem (Backend)
   ↓
Data Sources:
   - Oracle Database
   - AWS S3
   - Global Rules Engine
```

---

## Project Structure

```
project_folder/
│
├── payroll.py        # Backend logic (PayrollManagementSystem)
├── gui.py            # GUI application (PayrollGUI)
├── README.md         # Project documentation
```

---

## --> How to Run

### 1 Install Python

Make sure Python 3.x is installed.

### 2 Install Dependencies (if required)

* Tkinter (comes pre-installed with Python)
* Oracle DB connector (if used in backend)

### 3 Run the Application

```bash
python gui.py
```

### 4 Usage

* Enter employee name
* Click **"Calculate Salary"**
* View salary breakdown

---

##  How It Works

1. User enters employee name in GUI
2. GUI sends request to backend
3. Backend:

   * Connects to Oracle Database
   * Loads data from AWS S3
   * Applies global salary rules
   * Calculates salary
4. Results are returned to GUI
5. GUI displays formatted output

---

##  Error Handling

* Empty input → Warning popup
* Backend failure → Error popup

---

##  Future Enhancements

*  Dropdown for employee selection
*  Export salary report (PDF/Excel)
*  User authentication system
*  Improved UI design
*  Convert into web app (Flask/Django)

---

##  Author

Developed as part of learning:

* Python (Tkinter GUI)
* Backend integration
* Payroll processing logic
* Real-world application design

---

##  Notes

* Ensure `payroll.py` backend is properly configured
* Oracle DB and AWS S3 connections must be valid
* Salary rules should be defined correctly

---

##  Getting Started

Clone the repository:

```bash

git clone https://github.com/eswaracharimundlamuri/payroll_management_system

```

ADD ACCESS KEYY to it



