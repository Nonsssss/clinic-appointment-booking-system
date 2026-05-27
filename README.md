# Clinic Appointment Booking System
A full-stack, web-based platform designed to simplify, digitize, and automate clinic scheduling. This decoupled client-server application replaces manual, paper-based workflows with an intuitive online platform that enables patients to request appointments and clinic administrators to efficiently manage them.

---

## Objectives

* **Process Automation: Replace manual, paper-based scheduling with an accessible online system.
* **Resource Optimization: Implement logic-driven validation to eliminate overlapping bookings and maximize clinic resource utilization.
* **Systems Integration: Demonstrate a reliable architecture linking a responsive user interface, a secure backend API, and a relational database.
* **Modern DevOps Deployment: Establish environment parity through containerization and automate verification and delivery via a continuous integration and continuous deployment (CI/CD) pipeline.

---

## System Features
* **Role-Based Authentication: Distinct, secure access portals for patients and clinic administrators backed by stateless validation metrics.
* **Concurrency Validation: A booking core engineered with structural constraints to prevent duplicate or conflicting slot allocations.
* **Lifecycle Tracking: Real-time state management for submitted requests, updating dynamically across Pending, Approved, and Rejected statuses.
* **Administrative Control Panel: A centralized dashboard providing clinic personnel with the oversight to review and process pending requests.

---

## User Roles

1. **User / Patient: Authenticates into the application, browses available medical services and personnel, selects operating time blocks, and tracks the real-time status of their appointment requests.
2. **Admin / Clinic Personnel: Logs into the administrative dashboard, monitors incoming requests system-wide, and holds the authority to approve or reject requests to modify booking states.

---

## System Design & Architecture
The system utilizes a decoupled client-server architecture model to isolate concerns and ensure modular scalability:

* **Frontend Presentation Layer: Built using standard HTML, CSS, and JavaScript.
* **Backend Application Layer: Powered by Python with FastAPI.
* **Database Persistence Layer: Powered by MySQL.
* **DevOps Infrastructure: Uses Docker, GitHub Actions, and cloud deployment.

---

## Database Design
* **Users Table:** Stores patient and administrator account metadata, including full names, email addresses, and encrypted passwords for secure authentication.
* **Doctors Table:** Houses tracking metrics for clinic medical staff, storing their unique identification numbers and specialized areas of practice.
* **Services Table:** Details the specific medical services provided by the clinic, cataloging service duration, required slot parameters, and the specific doctor assigned to handle each package.
* **Appointments Table:** Records all booking transactions, establishing structural cross-references between patient profiles, assigned doctors, selected services, timetables, block allocations, and real-time status.

---

## API Documentation Reference

### Authentication Endpoints
* `POST /api/login` - Authenticates user profiles and distributes stateless validation credentials.

### Appointment Endpoints
* `GET /api/appointments` - Retrieves appointment history and structural data.
* `POST /api/appointments/book` - Submits a new appointment booking payload to the validation core.
* `PUT /api/appointments/status` - Modifies the lifecycle status of an existing appointment record (Admin privileges required).
* `GET /api/appointments/status` - Tracks the current real-time status of submitted requests.

---

## Implementation & Setup
The system architecture implementation relies on five distinct execution tracks:
1.  **Environment Standardization:** Handled via custom multi-container **Docker** definitions.
2.  **Schema Deployment:** Executed via structured **MySQL** database definition scripts.
3.  **Application Logic Engineering:** Created using **FastAPI** backends and type-safe **Pydantic** models.
4.  **Interface Development:** Implemented via a vanilla **HTML, CSS, and JavaScript** stack.
5.  **CI/CD Integration:** Automated testing, code verification, and deployment builds handled via **GitHub Actions**.

---

## 🧪 Testing Metrics & System Status
The following matrix tracks QA test scenarios, identifying critical compliance objectives along with current system performance status:

| Test ID | Feature Target | Test Scenario / Action | Expected Performance Target | Actual Performance Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Login Validation | Leave email and password empty. | System blocks login. | Login blocked successfully. | <span style="color:green;font-weight:bold;">PASS</span> |
| **TC-02** | Time Scheduling | Book appointment with exact time. | Correct time is saved. | Correct time saved successfully. | <span style="color:green;font-weight:bold;">PASS</span> |
| **TC-03** | Record Insertion | Submit invalid appointment form. | Invalid data should not save. | Failed information still saved in appointments. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-04** | Overlap Checking | Book already reserved schedule. | Duplicate booking blocked. | Duplicate booking allowed. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-05** | Booking Workflow | Submit appointment request. | Status becomes Pending. | Pending status displayed. | <span style="color:green;font-weight:bold;">PASS</span> |
| **TC-06** | Admin Panel | Open admin dashboard. | Appointment list loads. | Dashboard loaded correctly. | <span style="color:green;font-weight:bold;">PASS</span> |
| **TC-07** | Status Sync | Approve appointment request. | Status changes to Approved. | Status updated successfully. | <span style="color:green;font-weight:bold;">PASS</span> |
| **TC-08** | Responsive UI | Open system on mobile. | Layout adjusts properly. | UI layout broken on small screens. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-09** | Dialog Box | Trigger form error. | Clean message displayed. | Code lines appeared in dialog. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-10** | Contact Validation | Enter letters in contact number. | Only numbers accepted. | Letters and symbols accepted. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-11** | Age Validation | Enter very large age. | Invalid age blocked. | Infinite age accepted. | <span style="color:red;font-weight:bold;"> FAIL</span> |
| **TC-12** | Registration Email | Create new account. | Email notification sent. | No email notification. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-13** | Status Notification | Approve or reject appointment. | User receives email update. | No email notification. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-14** | Rejection Feedback | Reject appointment request. | User sees rejection reason. | No rejection feedback. | <span style="color:red;font-weight:bold;">FAIL</span> |
| **TC-15** | Password Visibility | Open login password field. | Eye icon available. | No eye icon available. | <span style="color:red;font-weight:bold;">FAIL</span> |