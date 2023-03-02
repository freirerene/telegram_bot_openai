# OpenAI telegram bot

This is a trivial implementation of the OpenAI API in a telegram bot -- so the bot becomes an interface
to the ChatGPT.

The new model `gpt-3.5-turbo` the powers ChatGPT is now available as an API, and is much cheaper than the previous
most powerful model from OpenAI.

## Implement it on AWS

First, create your lambda function. Then, in `API Gateway` create an `API HTTP` with the option `Integration` as the 
Lambda you created: the URL `https://your-apigateway.amazonaws.com` is created. In `Routes` inside `API Gateway`
there's the route created, for instance, `telegram_webhook`.

Second, create the webhook using REST POST `https://api.telegram.org/bot{BOTKEY}/setWebhook`
setting, in the body, `url=https://your-apigateway.amazonaws.com/telegram_webhook`

And the rest is the usual creation of layers with the libraries, etc.