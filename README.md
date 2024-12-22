[![Maintainability](https://api.codeclimate.com/v1/badges/e0080a631100f636c310/maintainability)](https://codeclimate.com/github/PavelZ94/OccupationalSafety/maintainability)
[![lint_check](https://github.com/PavelZ94/OccupationalSafety/actions/workflows/lint-check.yml/badge.svg)](https://github.com/PavelZ94/OccupationalSafety/actions/workflows/lint-check.yml)

# OccupationalSafety Telegram Bot

## About
This is Telegram bot, created with a purpose to commit violations of Occupational Safety on factory and send information about it to Occupational Safety Department.

## Usage


It supports next messages:

1) ```/mistake``` - to commit the violation;
2) ```/help``` - to see information about Near-Miss conception and why it is so important.

## Sending mistakes

Sending information about violation contain next steps:
1) sending name of user;
2) sending brief information about violation;
3) sending detailed description about violation;
4) choosing the importance level;
5) sending information about place, where violation has happened;
6) sending a photo showing a violation.

After that, HSE Department of factory get information about Near-Miss event.
It registers with unique number.

The user receives a message that his application has been registered. He also sees the application number information so he can verify that it is registered and can track its progress.