# Gaic Platform Health Check
This Platform_Health_Check.exe provides a health check utility for managing and monitoring a gaic platform. It performs various checks, such as database connectivity, license validation, disk space monitoring, and service statuses, while generating an HTML report summarizing the results.

### Features
- **Database Connection Check**: Validates connectivity to a PostgreSQL database (CSS).
- **License Key Validation**: Verifies license keys in both CSS and the console.
- **Disk Space Monitoring**: Ensures sufficient disk space on the specified drive.
- **Service Checks**: Monitors AIP Console version, services like HDED, and imaging status.
- **HTML Report Generation**: Creates an HTML report summarizing health checks.

### Prerequisites
To run Platform_Health_Check.exe we need below details. These details should be there
inside Customer_Platform_Health_Check_Settings.json file.


Example JSON Structure

```json
{
  "jira": {
    "msinfra_ticket_no": "",
    "url": "https://cast-delivery.atlassian.net/"
  },
  "html_file_path": "https://gaicreport.corp.castsoftware.com/",
  "css": {
    "database": "css_database",
    "user": "css_user",
    "password": "css_password",
    "host": "css_host",
    "port": 2284
  },
  "console": {
    "restURL": "http://console.rest.url/",
    "user": "console_user",
    "password": "console_password"
  },
  "warnDays": 15
}
```
Update the Platform_Health_Check_Settings.json file with the appropriate database, console, and user configurations.

### How It Works
The Platform_Health_Check.exe performs a series of automated operations to ensure the health and functionality of the system. Below is the detailed workflow:


**1. Configuration Setup:**
- The script locates the Platform_Health_Check_Settings.json file in the following directory:
```bash
C:\CAST\Platform_Health_Check
```
- This file contains critical configuration values, including:

	1.  Warn Days
	2.  Jira URL
	3.  HTML File Path
	4.  CSS Database Name, Username, Password, Host, and Port
	5.  AIP Console Rest URL and Credentials

- Note: Jira Username, Jira Password, and EXE Version are hardcoded.

**2. Log File Creation:**
- The script creates a log file named Platform_Health_Check_Logs.txt in the same directory to record all actions and errors.

**3. Jira Integration:**

- Retrieves the corresponding MSINFRA Ticket for the VM from Jira.
- Updates the MSINFRA Ticket number in the Platform_Health_Check_Settings.json file.

**4. Updating Credentials:**
- The script updates the AIP Console credentials (Username and Password) inside the JSON file.
- If the credentials are invalid, they are replaced with default values (admin/admin or cast/cast).

**5. CSS Configuration Update:**
- Fetches the CSS port number and hostname from the AIP Console.
- Updates the CSS Port and CSS Hostname in the JSON configuration file.

**5. Fetching Data from AIP Console:**
- Retrieves the License Key from the console.
- Fetches the list of applications along with their details from the console.

**6. Updating License Keys:**
- Updates the License Key for each application in the CSS database table (sys_licenses).

**7. Health Checks:**
Performs various health checks, including:

- **Current Date Time and Host Name**
- **Application Details**
- **CSS Status:** Validates database connectivity.
- **License Key Status:** Verifies license key validity in CSS and Console.
- **Disk Space:** Checks if sufficient disk space is available on the C: drive.
- **HDED Service Status:** Ensures the HDED service is running and its URL is functional.
- **Imaging Status:** Confirms whether imaging is properly loaded.

**8. Generating an HTML Report:**
- Collects data such as:
	1. 	Current Date and Time
	2. 	Host Name
	3. 	Application Details
- Creates an HTML file summarizing the results in a table format.
- Saves the file in the following directory:- C:\CAST\Platform_Health_Check
- Copies the file to the remote path:
```bash
\\gaicreport.corp.castsoftware.com\wwwgaicreport
```

**9. Error Reporting and Ticket Updates:**

- If any KO, WARN, or ERR statuses are detected, updates the MSINFRA Ticket.
- Updates the ticket with the remote path of the HTML report.

**10. Jira Dashboard Integration:**

- The script integrates with a Jira dashboard to monitor all GAIC VMs on a single page:
- GAIC VMs Dashboard -> https://cast-delivery.atlassian.net/jira/dashboards/10001

### Deployment
To deploy the Platform_Health_Check.exe, a secondary executable, Launcher.exe, is used to manage deployment:

**1. Version Comparison:**

- Compares the version of Platform_Health_Check.exe in the local directory - **C:\CAST\Platform_Health_Check** with the version in the remote directory -**\\gaicreport.corp.castsoftware.com\wwwgaicreport\apps**

**2. Copying Updates:**

- If the versions differ, Copies the updated Platform_Health_Check.exe from the remote path to the local path.
- If the versions are the same, no action is taken.

**3. Upgrades/Downgrades:**

- To upgrade or downgrade Platform_Health_Check.exe, place the desired version in the remote path.

**4. Scheduled Tasks:**

- Both Launcher.exe and Platform_Health_Check.exe are scheduled tasks on a Template VM.
- When a new VM is created, these tasks are automatically available.


### Main Functionalities(Methods):
- **update_console_username_and_password(json_file)**:- Updates the username and password in the JSON configuration file if default credentials are detected.

- **update_css_details(json_file, host_name)**:- Updates CSS database configuration in the JSON file with the latest port and host details.

- **get_applications_from_console()**:- Fetches application details from the console.

- **get_the_license_from_the_console()**:- Retrieves the license key details from the console.

- **update_application_license_key(app_local_schema, console_license_key)**:- Updates the application license key in the CSS database.

- **check_postgres_status()**:- Verifies the status of the PostgreSQL database.

- **check_diskspace()**:- Checks the available disk space on the system.

- **is_aip_console_version_2x()**:- Checks if the AIP Console version is 2.x.

- **check_HDED()**:- Validates the status of the HDED service and its associated URL.

- **check_imaging_loaded()**:- Confirms whether imaging is loaded.

- **create_html_table(data, host_name, current_date_time, exe_version)**:- Generates an HTML table for the health check results.

### Logs
The script logs details of its execution at:
```bash
C:\CAST\Platform_Health_Check\Platform_Health_Check_Logs.txt
```

### Error Handling
- Errors during execution are logged for debugging purposes.
- The script provides meaningful messages for configuration or runtime issues.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.



### Support

If you encounter any issues or have questions, please contact s.p@castsoftware.com

