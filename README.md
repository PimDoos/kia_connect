# MyKia / Kia Connected Services
This custom component integrates MyKia into Home Assistant.

Setup with HACS
---------------
Add this repository to your custom repositories.


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
- Base URL, e.g. `https://mykia.com`
- A json response for the `/api/user` call
- A json response for the `/api/vehicles/{preferred_vehicle}/connected-status` call

Please anonymize these json values before submitting.


Screenshots
-----------
![image](https://user-images.githubusercontent.com/17709721/163465456-6a9a3fc9-5770-4aea-a06c-fcca0107eb6f.png)
