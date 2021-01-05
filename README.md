# Discord Reddit Fetcher
This is a simple discord bot written in python, utilizing the reddit json api to get info about media on a subreddit and posts it to a discord channel.

# Installation
1. Clone the github repo.
2. Invite your bot to your discord server, you can do this with the url `https://discord.com/oauth2/authorize?client_id={YOUR DISCORD BOTS CLIENT ID}&scope=bot`
3. Create a file called `discordBotSecret.txt` and paste your discord bot client secret that you can find at https://discord.com/developers/applications
4. Run the program as `.pyw` or `.py`
5. Upon running the program you will find a file created called `pid.txt` this is the programs process id. This is useful if you run the program as `.pyw`

# Usage
On your discord server type `!rf {subreddit name}` and the bot will fetch a random image from the subreddit. If it can't it will tell you the error.
Example: `!rf memes`

Sources used: https://discordpy.readthedocs.io/en/latest/
