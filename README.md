# Akacia bots
Simple Telegram bots for [Akacia apartments](https://akacia.me/)

## The problem
People in Akacia wants to know current situation about payments, bills, and balance.

## Solution
I created two bots: one for Akacia's renters, one for Akacia's managment.
Renter can check bills, list payments, ask for balance.
Manager can add payment and get information about any apartment in Akacia.

## Files

* **common.py** — constants, templates, common functions.
* **bot.py** — main bot
* **payments_bot.py** — manager's bot
* **sender_total.py** — helper file for sending information to subscribers
