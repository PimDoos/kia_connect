# MijnKia / Kia Connected Services
This custom component integrates MijnKia (Connected Car Services) into Home Assistant.

This implementation is specific to the non-UVO Kia Connected Services implementation for cars built before 2021.
Newer cars mostly use the Kia UVO implementation. See [fuatakgun/kia_uvo](https://github.com/fuatakgun/kia_uvo/) to integrate with those.

Setup with HACS
---------------
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

This repository is available in the HACS default repository.


Manual Setup
------------
Copy the kia_connect folder to your custom_integrations folder.

After installing, you can set the integration up from the UI:

![image](https://user-images.githubusercontent.com/17709721/163856070-88a2a764-ab1d-4ece-a8d2-d46161cbe9f5.png)


Tested cars
-----------
| Model | Type |
|-------|------|
| Kia e-Niro | EV |

Supported regions
-----------------
These regions are currently supported. 

| Region | MyKia URL |
|--------|-----------|
| Netherlands (NL) | https://mijnkia.nl |

Want your region added? Log in to your MyKia account and open an issue with the following information:
- Base URL, e.g. `https://mijnkia.nl`
- A json response for the `/api/user` call
- A json response for the `/api/vehicles/{preferred_vehicle}/connected-status` call

Please anonymize these json values before submitting.


Screenshots
-----------
![image](https://user-images.githubusercontent.com/17709721/163465456-6a9a3fc9-5770-4aea-a06c-fcca0107eb6f.png)
