Splunk Shells App
Version 1.0

TBG Security
Ryan Hays

This app is to help with penetration testing and Red Teaming within environments that have a Splunk deployment.

This app will allow the engineer to spawn a Reverse of Bind Shell from a Splunk server to allow the engineer to
interact with the server and expand influence within the environment.

= Install =
Download the release from <INSERT RELEASE URL>

Navigate to the "Manage Apps" and click on "Install app from file"

![Alt text](appserver/static/splunk_apps.png?raw=true "Optional Title")

Click on "Choose File" and select the downloaded release archive.

![Alt text](appserver/static/splunk_install.png?raw=true "Optional Title")

Once it is installed you will have to restart Splunk

![Alt text](appserver/static/splunk_restart.png?raw=true "Optional Title")

For Splunk v6.5 ONLY
Once Splunk is restarted click on Permissions for the splunk_shells app. Ensure the last permission "Sharing for config file-only objects" has "all apps" selected.

![Alt text](appserver/static/splunk_permissions.png?raw=true "Optional Title")
