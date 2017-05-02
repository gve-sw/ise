## ASE AMERICAS Team 2 - Software Project Q3FY17
This repository contains code for the software project of ASE AMERICAS Team 2.

The project is organized in a 3 step process, notably:
* **Step 1** - Collect/streamline/write basic scripts for common tasks/operations of the main Cisco APIs
* **Step 2** - Build a 'Wrapper' API for the basic scripts in step 1
* **Step 3** - Write a simple use case that leverage the 'Wrapper' API. The use case may also leverage APIs outside the core ones, e.g., Spark & Tropo for human interaction.

You will find the corresponding folders for each step.


### Team Members
* Mike Castellana
* Chiara Pietra


### Coaches/Sponsors
* Robert E Roulhac (Main coach)
* Cosmina Calin
* Jina Park
* Fernando Urdapilleta
* Hugo Tamayo
* Pedro Castro


### Products in this project
* [Cisco Identity Services Engine](http://www.cisco.com/c/en/us/products/security/identity-services-engine/index.html)


### API Documentation
* [Cisco Identity Services Engine - Reference Guides] (http://www.cisco.com/c/en/us/support/security/identity-services-engine/products-command-reference-list.html)


“””
* [DevNet pxGrid Resources](https://developer.cisco.com/site/pxgrid/)
* [Cisco Umbrella Investigate API](https://investigate-api.readme.io/)
“””

### Sample Application

When using ISE for Guest wireless, we can choose the self-registration option to allow users to connect to the wireless network. A sponsor has to approve that user, allowing him (or not) to get access to the network.
The sponsor can approve the user using the Sponsor’s portal on ISE or via email.

This project has two main goals:
- As we know that there is a guest that is trying to connect to the network, we can use the information that provides to ISE and print a temporary badge in order to identify himself inside the company.
- Allow the sponsor to approve the guest users that are asking to connect to the network through the use of a Spark room. This is another option besides the Sponsor’s portal and email. 