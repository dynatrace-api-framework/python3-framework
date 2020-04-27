# Examples

## Use Cases - Aaron/"Philly"

### Weekly Metrics
I report the number of users, the number of applications onboarded, and number of hosts that are being monitored by Dynatrace.<br/>
Check out the "examples" git branch for aaron_weekly_metrics.py

### List of Host Groups
We keep a document of all the different Host Groups that we are using. So I use a script occasionally to update the document of all the host groups in each environment.<br/>
Check out the "examples" git branch for aaron_host_groups.py

### Host Units by Management Zone
Like many clients, my client uses a single tenant for NonProd and another tenant for Prod. Application teams are split by Management Zones. To track how many host units each team is using, I created a script to get the number of Host Units in use by each team.

### Onboarding New Applications
When onboarding a new application, I run this script. It will create all the user_groups required as well as the management zones needed for the different lifecycles of the application

### Backend for Django Project
Implementing this project as a backend for a Django-based web application. Stay tuned!