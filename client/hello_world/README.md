# Hello_world.py

A 'hello world' plugin to serve as a basic template and demonstration. This plugin will display a message box when King Phisher exits.

## Getting Started

These instructions will get you a copy of the plugin up and running on your local machine for development and testing purposes. 

### Prerequisites

What you need to install the software and how to install them:

```
Linux or Windows 
Python Minimum Required Version = 3.3.0
King Phisher Minimum Required Version = 1.4.0 
Advanced HTTP Server 
```

### Installing 

- [ ] Download plugin 
- [ ] Move plugin to: <code>/opt/king-phisher-plugins/client/</code>
- [ ] Configure plugin<code>(refer to Deployment & Configuration below)</code> 

## Running the tests

In order to test if hello_world.py is operational, exit King Phisher. On exit, a message box will display either with the default options or your own options. The example below is with default options: 
```
Good bye Alice Liddle!
```
## Deployment & Configuration 

On line 24 of hello_world.py is the start of Client Options. If the client does not specify the Client Options, the client will recieve default values for those options. 

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
    hello_world:
      display_name="Alice"
      validiction=False
      some_number=2121 
      tcp_port=8080
```

### Client Side Plugin Manager
In addition to implementing our own configurations into the server_config.yml file, the King Phisher Client is equiped with a `Plugin Manager.` This Plugin Manager contains the toggleable `Installed` and `Enabled` features, both Installed and Enabled checkboxes *must* be checked before use of any King Phisher plugins.  

## Authors

* **Spencer McIntyre** - *Plugin Author* - [zeroSteiner](https://github.com/zeroSteiner)
* **Austin DeFrancesco** - *Documentation Author* - [ninedeaths](https://github.com/ninedeaths)
* **

See also the list of [contributors](https://github.com/securestate/king-phisher/contributors) who participated in this project.

## License

This project is licensed under the BSD 3-Clause "New" or "Revised" License - see the [LICENSE.md](https://github.com/securestate/king-phisher/blob/master/LICENSE) file for details

## Acknowledgments

* Thank you to the contributers and end users that make up the King Phisher community. 
