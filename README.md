# TruCtrl

---

### **What is TruCtrl?**

**TruCtrl** is a modern IT security management and compliance platform designed to streamline the implementation of the **CIS Controls** framework through integrated asset tracking, configuration management, and control verification.

Built on a **FastAPI backend** and a **Next.js frontend**, TruCtrl is a fast, modular, and open-source system intended for IT professionals who need actionable security visibility across hybrid infrastructures.

---

### **Key Features:**

* **CIS Controls Compliance Framework**
  Maps and tracks CIS Controls v8 safeguards across systems and departments. Provides automated documentation, control ownership, and progress tracking toward full implementation.

* **CMDB + ITAM Hybrid**
  Maintains relationships between assets, users, configurations, and security controls. Tracks lifecycle data and integrates with external platforms for real-time state awareness.

* **Rich API Integrations**
  Designed to pull data from and push updates to systems like:

  * **Azure AD / Active Directory** (SSO and user correlation)
  * **Meraki** and **vSphere** (network and virtualization layers)
  * **ManageEngine** and **ServiceDesk Plus** (incident/ticket linkage)

* **Web Interface + Automation Hooks**
  A polished Next.js interface for management and reporting, with API and CLI endpoints for automation, scripting, and external system integration.

* **Role-Based Access Control (RBAC)**
  Granular permission management to ensure least-privilege access to sensitive data and controls.

* **Security Alerts & Drift Detection**
  Detects and notifies on unauthorized configuration changes, unmanaged assets, or deviations from expected security postures.

---

### **Designed For:**

* **IT operations teams** needing a lightweight but extensible tool to operationalize CIS Controls.
* **Security-conscious organizations** who want visibility and control without resorting to bloated enterprise GRC platforms.
* **Hybrid and multi-campus environments**, especially in education, healthcare, or mid-sized enterprise networks.

---

## Setup Instructions

To clone all subproject repositories and set up Python and Node.js environments (where applicable), use the provided setup scripts:

### Windows (PowerShell)

Run the following command in PowerShell:

```powershell
./setup.ps1
```

### macOS/Linux (Shell)

Run the following command in your terminal:

```sh
sh setup.sh
```

These scripts will:
- Clone each subproject repository if it does not already exist.
- For subprojects with a `requirements.txt`, create a Python virtual environment and install dependencies automatically.
- For subprojects with a `package.json`, install Node.js dependencies using npm or yarn.

