# Clockwork SMS

Send SMS messages using the Clockwork SMS API's email gateway. While enabled, this plugin will automatically update phone numbers into email addresses for sending using the service.

## Getting Started

These instructions will get you a copy of the plugin up and running on your local machine for development and testing purposes. 

### Prerequisites

What you need to install the software:

```
Linux or Windows 
King Phisher Minimum Required Version = 1.0.1 
ClockWork API with credits (https://www.clockworksms.com/)
```

### Installing

- [ ] Use King Phisher Clients plugin manager to install and enable
>It is recommended that end users implementing this plugin run the King Phisher Client in debug mode before testing the plugin. `DEBUG` is accomplished by inserting `-L DEBUG` onto the execution command. 


## Running the tests

In order to test if clockwork_sms.py is operational, we must send out a phishing attempt. Within the following King Phisher Client tabs: `Send Messages -> Configuration -> Target Information.` Once within the target information field, enter the number in which you want to target. Once the proper information is inputted, we need to change to the `Send` tab within the King Phisher Client. Once there we can send our phishing attempt out. 

Once `DEBUG` logging has been enabled, send out the phishing attempt and keep an eye on the `DEBUG` logging. If you see any `WARNING` within the log, check your configurations and begin the README process again. 

## Deployment & Configuration 

If the client does not specify the Client Options, the client will receive default values for those options. 

To implement your options navigate to the toolbar, `EDIT -> PREFRENCES -> PLUGINS` within the King Phisher Client. 

###Client Side Plugin Manager
This Plugin Manager contains the `Installed` and `Enabled` features, both Installed and Enabled checkboxes *must* be checked before use of any King Phisher plugins.  

## Authors

* **Spencer McIntyre** - *Plugin Author* - [zeroSteiner](https://github.com/zeroSteiner)
* **Austin DeFrancesco** - *Documentation Author* - [ninedeaths](https://github.com/ninedeahts)
* **

See also the list of [contributors](https://github.com/securestate/king-phisher/contributors) who participated in this project.

## License

This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the [LICENSE.md](https://github.com/securestate/king-phisher/blob/master/LICENSE) file for details

## Acknowledgments

* Thank you to the contributors and end users that make up the King Phisher community.
