# CurrencyConverter

CurrencyConverter is a script to indicate the conversion rates of different currencies in a popup message.
Initially, this is developed to check the conversion rates from SEK to INR and to achieve this, we have took TransferWise website as a reference.

I hope we can use this script for other currencies as well by changing some parameters (from_currency, to_currency and corresponding url) in conversion_details.json file,and it is successfully tested for SEK to INR conversions.

{
	
	"url": "https://transferwise.com/gb/currency-converter/sek-to-inr-rate?amount=1",
	
	"from_currency": "SEK",
	
	"to_currency": "INR",
	
	"interval": 60
	
}

