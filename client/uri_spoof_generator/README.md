# URI Spoof Generator 

Exports a redirect page which allows URI spoofing in the address bar of the target's browser.

## Getting Started

These instructions will get you a copy of the plugin up and running on your local machine for development and testing purposes. 

### Prerequisites

What you need to install the software:

```
Linux or Windows 
King Phisher Minimum Required Version = 1.0.1 
```

### Use King Phisher Plugin Manager to install and enable plugin

- [ ] Download plugin 
- [ ] Move plugin to: `/opt/king-phisher-plugins/client/`
- [ ] Configure plugin `(refer to Deployment & Configuration below)` 

## Running the tests

In order to test if `uri_spoof_generator.py` is operational, we must send out a phishing attempt. Navigate within the following King Phisher Client tabs: `Send Messages -> Configuration -> Target Information.` 

In order to create the URI redirect, navigate to the toolbar, `EDIT -> PREFRENCES -> PLUGINS` within the King Phisher Client. 
After target information has been filed, we need to configure and create the URI redirect. Navigate to `TOOLS -> Create Data URI Phish` 

```
Redirect URL: <SHOULD BE YOUR KINGPHISH SERVER> 
Spoofed URI: <SHOULD BE THE SPOOFED URL> 
Output HTML File: <PATH TO SAVE YOUR HTML FILE> 
``` 

[URI attacking requires more information than this README will supply. The following URL is a good starting point on how to properly use the URI Spoofing Plugin.](https://youtu.be/Zlk76Oqw7Oo)

>It is recommended that end users implementing this plugin run the King Phisher Client in debug mode before testing the plugin. `DEBUG` is accomplished by inserting `-L DEBUG` onto the execution command. 

Once `DEBUG` logging has been enabled, send out the phishing attempt and keep an eye on the `DEBUG` logging. Once target opens phishing URL, the redirect should dispatch onto a new tab within the browser window. If you see any `WARNING` or `CRITICAL` within the log, check your configurations and begin the README process again. 

## Deployment & Configuration 

If the client does not specify the Client Options, the client will receive default values for those options. 

To implement your options navigate to the toolbar, `EDIT -> PREFRENCES -> PLUGINS` within the King Phisher Client. 

###Client Side Plugin Manager
This Plugin Manager contains the `Installed` and `Enabled` features, both Installed and Enabled checkboxes *must* be checked before use of any King Phisher plugins.  

## Authors

* **Jeremy Schoeneman** - *Plugin Author* - [y4utj4](https://github.com/y4utj4)
* **Austin DeFrancesco** - *Documentation Author* - [ninedeaths](https://github.com/ninedeahts)
* **

See also the list of [contributors](https://github.com/securestate/king-phisher/contributors) who participated in this project.

## License

This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the [LICENSE.md](https://github.com/securestate/king-phisher/blob/master/LICENSE) file for details

## Acknowledgments

* Thank you to the contributors and end users that make up the King Phisher community.
