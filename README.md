# MijnKia

This custom component integrates MijnKia (Connected Car Services) into Home Assistant.

## Choose the right integration

This implementation is specific to Dutch Kia cars built before 2021, connected to the [MijnKia app](https://play.google.com/store/apps/details?id=com.redhotminute.kia.mijnkia).

If your car works with the modern [Kia App](https://play.google.com/store/apps/details?id=com.kia.oneapp.eu), please use the [kia_uvo](https://github.com/Hyundai-Kia-Connect/kia_uvo) integration.

## Setup

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

This repository is available in the Home Assistant Marketplace.

[![Open your Home Assistant instance and open a repository in the Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=PimDoos&repository=kia_connect&category=plugin)

After installing, you can set the integration up from the UI:

![image](https://user-images.githubusercontent.com/17709721/163856070-88a2a764-ab1d-4ece-a8d2-d46161cbe9f5.png)

### Manual setup

Copy the kia_connect folder to your custom_integrations folder.



## Tested cars

| Model | Type |
|-------|------|
| Kia e-Niro MY19 | EV |

## Supported regions

These regions are currently supported. 

| Region | MyKia URL |
|--------|-----------|
| Netherlands (NL) | https://mijnkia.nl |



Screenshots
-----------
![image](https://user-images.githubusercontent.com/17709721/163465456-6a9a3fc9-5770-4aea-a06c-fcca0107eb6f.png)
