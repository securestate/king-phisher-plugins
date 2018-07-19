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

### Installing 

- [ ] Download plugin 
- [ ] Move plugin to: <code>/opt/king-phisher-plugins/client/</code>
- [ ] Configure plugin<code>(refer to Deployment & Configuration below)</code> 

## Running the tests

In order to test if `uri_spoof_generator.py` is operational, we must send out a phishing attempt. Navigate within the following King Phisher Client tabs: `Send Messages -> Configuration -> Target Information.` Once within the target information field, enter the target. Once the proper information is inputted, we need to change to the `Send` tab within the King Phisher Client. Once there we can send our phishing attempt out. 

>It is recommended that end users implementing this plugin run the King Phisher Client in debug mode before testing the plugin. `DEBUG` is accomplished by inserting `-L DEBUG` onto the execution command: 
```
# CLIENT EXAMPLE 
testing@testVM:/opt/king-phisher$ ./KingPhisher -L DEBUG
```
```
# SERVER EXAMPLE 
testing@testVM:/opt/king-phisher$ sudo ./KingPhisherServer server_config.yml -L DEBUG
```

Once `DEBUG` logging has been enabled, send out the phishing attempt and keep an eye on the `DEBUG` logging. Once target opens phishing URL, the redirect should dispatch onto a new tab within the browser window. If you see any `WARNING` or `CRITICAL` within the log, check your configurations and begin the README process again. 

## Deployment & Configuration 

On line 22 of `uri_spoof_generator.py` is the start of `Client Options`. If the client does not specify the `Client Options`, the client will receive default values for those options. 

To implement your options to <code>Client Options</code>, navigate to <code>/king-phisher/server_config.yml</code> 

Once server_config.yml is open, navigate to <code>#plugins</code> within the file. Here we will implement our own options:
>Note that proper spacing is critical to the server_config.yml file.
```
#EXAMPLE
  Two spaces
    Four spaces
      Six spaces
```

```
#EXAMPLE
  plugins: 
    uri_spoof_generator:
      redir_url = 'example.com' 
      spoofed_uri = 'spoofedUI' 
      output_html_file = '~/redirect.html' 
```
###Client Side Plugin Manager
In addition to implementing our own configurations into the server_config.yml file, the King Phisher Client is equipped with a `Plugin Manager.` This Plugin Manager contains the `Installed` and `Enabled` features, both Installed and Enabled checkboxes *must* be checked before use of any King Phisher plugins.  

## Authors

* **Jeremy Schoeneman** - *Plugin Author* - [y4utj4](https://github.com/y4utj4)
* **Austin DeFrancesco** - *Documentation Author* - [ninedeaths](https://github.com/ninedeahts)
* **

See also the list of [contributors](https://github.com/securestate/king-phisher/contributors) who participated in this project.

## License

This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the [LICENSE.md](https://github.com/securestate/king-phisher/blob/master/LICENSE) file for details

## Acknowledgments

* Thank you to the contributors and end users that make up the King Phisher community.