# Campaign Message Configuration

Store campaign message configurations for their respective campaigns. This allows users to switch between campaigns while keeping each of the message configurations and restoring them when the user returns to the original campaign. New campaigns can either be created with customizable default
settings or from the existing configuration (see the "Transfer Settings" option).

## Getting Started

These instructions will get you a copy of the plugin up and running on your local machine for development and testing purposes. 

### Prerequisites

What you need to install the software:

```
Linux or Windows 
King Phisher Minimum Required Version = 1.10.0 
```

### Installing
- [ ] Use King Phisher Clients plugin manager to install and enable
>It is recommended that end users implementing this plugin run the King Phisher Client in debug mode before testing the plugin. `DEBUG` is accomplished by inserting `-L DEBUG` onto the execution command. 

## Running the tests

In order to test if `campaign_message_configuration.py` is operational, we must change campaigns then return back to the original campaign. To create a new campaign, navigate to the King Phisher Client.
Once inside of the client we need to open the campaigns menu, to do this go to `File -> Open Campaign -> New Campaign. After you have generated a new campaign, revert back to the original campaign that you created and check that your settings, etc.. If all campaign information is being saved and properly carried over then the plugin is working properly!  

## Deployment & Configuration 

If the client does not specify the `Client Options`, the client will receive default values for those options. 

To implement your options navigate to the toolbar, `EDIT -> PREFRENCES -> PLUGINS` within the King Phisher Client. 

### Client Side Plugin Manager
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
