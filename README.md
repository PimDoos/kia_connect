# kia_connect
Home Assistant Custom Component: Kia Connected Services

This custom component integrates MyKia into Home Assistant.

Setup with HACS
---------------
Add this repository to your custom repositories.


Manual Setup
------------
Copy the kia_connect folder to your custom_integrations folder.

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
- Base URL, e.g. `https://mykia.com`
- A json response for the `/api/user` call
- A json response for the `/api/vehicles/{preferred_vehicle}/connected-status` call

Please anonymize these json values before submitting.
