# niko_apartaments

## Hot to get channel id
1. Create a channel
2. Add your bot to the channel
3. Send a message ```/my_id @<your_bot_tag>```
4. Go to the ```https://api.telegram.org/bot<bot_api_token>/getUpdates``` link
5. Extract from JSON from a ```"id"``` field channel id