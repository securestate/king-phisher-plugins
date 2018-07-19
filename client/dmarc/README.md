# Phishery Docx

This plugin adds another safety check to the message precheck routines to verify that if DMARC exists, the message will not be quarantined or rejected. If no DMARC policy is present, the policy is set to none or the percentage is set to 0, the message sending operation will proceed.

## Getting Started

These instructions will get you a copy of the plugin up and running on your local machine for development and testing purposes. 

### Prerequisites

What you need to install the software:

```
Linux or Windows 
King Phisher Minimum Required Version = 1.5.0 
```

### Installing 

- [] Download plugin 
- [] Move plugin to: <code>/opt/king-phisher-plugins/client/</code>
- [] Configure plugin<code>(refer to Deployment & Configuration below)</code> 

## Running the tests

In order to test if `dmarc.py` is operational, we must send out a phishing attempt. Within the following King Phisher Client tabs: `Send Messages -> Configuration -> Target Information.` Once within the target information field, enter the target. Once the proper information is inputted, we need to change to the `Send` tab within the King Phisher Client. Once there we can send our phishing attempt out. 

It is recommended that end users implementing this plugin run the King Phisher Client in debug mode before testing the plugin. `DEBUG` is accomplished by inserting `-L DEBUG` onto the execution command: 
```
# CLIENT EXAMPLE 
testing@testVM:/opt/king-phisher$ ./KingPhisher -L DEBUG
```
```
# SERVER EXAMPLE 
testing@testVM:/opt/king-phisher$ sudo ./KingPhisherServer server_config.yml -L DEBUG
```

Once `DEBUG` logging has been enabled, send out the phishing attempt and keep an eye on the `DEBUG` logging. If you see any `WARNING` or `CRITICAL` within the log, check your configurations and begin the README process again. Else, if the plugin executed successfully, DMARC tags will be stripped out dependent upon the following domain variables: 
```
# DMARC Variables
record 
version 
policy 
```
## Deployment & Configuration 

This plugin does not contain any client options. 

### Client Side Plugin Manager
The King Phisher Client is equipped with a `Plugin Manager.` This `Plugin Manager` contains the `Installed` and `Enabled` features, both `Installed` and `Enabled` checkboxes *must* be checked before use of any King Phisher plugins.  

## Authors

* **Spencer McIntyre** - *Plugin Author* - [zeroSteiner](https://github.com/zeroSteiner)
* **Austin DeFrancesco** - *Documentation Author* - [ninedeaths](https://github.com/ninedeahts)
* **

See also the list of [contributors](https://github.com/securestate/king-phisher/contributors) who participated in this project.

## License

This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the [LICENSE.md](https://github.com/securestate/king-phisher/blob/master/LICENSE) file for details

## Acknowledgments

* Thank you to the contributors and end  users that make up the King Phisher community.
