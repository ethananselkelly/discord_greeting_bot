# Discord Greeting Bot AKA Hank Scorpio

## Video Demo: <https://youtu.be/1RwvoXKCZus>

## Description: Hank uses the Discord API via discord.py to welcome new users to a Discord server

### When a new user joins the Discord server, the event triggers Hank to make a GET request to the Tenor (gif) API for a Simpsons-related greeting, which he then sends to the Discord server's general text channel.

### Hank can also make a GET request to the Simpsons quote API and send the quote as a message in the text channel.

---

## The main file for Hank is final_project.py, and is made up of 4 main functions: run_bot(), get_gif(), get_gif_params(), and get_quote().

---

### run_bot() creates the client, which is the connection between the bot (Hank) and the Discord API, using the discord.py. This is where Hank specifies his intents, defines actions that trigger on certain events, and imports appropriate environment variables for the various APIs. There are 3 events that Hank listens for:

> on_ready(): this function is called when run_bot() is called, and it makes the connection to the Discord server (or GUILD). It prints a statement relaying this information.

> on_member_join(): this function is called when a new user joins the Discord server. This function calls the get_gif() function and sends the return value as a message in the server's text channel.

> on_message(): this function is called when a user sends a message in the server's text channel, and sends a response message based on the value of the user's message (str).

### run_bot() was the most complicated code to implement in this project, but it was fun to learn and get the hang of how to configure and use the Discord API, and there's a lot more functionality beyond what I'm doing here that opens up with the API.

---

### get_gif() makes a request to the Tenor API using the requests library. The function is passed variables for both the API and Client keys, which are required in order to make requests to Tenor. The search term for the request is supplied by the get_gif_params() function. The response body is parsed for the .gif url, and that url is returned as a str. Originally, the function defined the keys inside of the function, but this caused issues when writing tests for the function. Therefore, keys are passed as params, and the keys are defined in the parent function.

---

### get_gif_params() returns a str that is randomly selected from a list of search terms. In keeping with the spirit of the Discord server for which this bot was created, all of the list items are search terms that will return a Simpsons-related gif.

---

### get_quote() makes a request to the Simpsons quote API for a random quote. The response is an array of quotes (only one is returned here) and the quote along with it's character is returned as an f string

---

### The main() function only needs to call run_bot(), and the bot will stay active until it is disconnected using ^C on Mac

---

### TODO:

### -Implement Twitter API to GET random tweets from user @SimpsonsQOTD

### -Use Discord commands (!command syntax) to avoid accidentally triggering an event response by Hank

### -Deploy Hank to a cloud server so that it can stay up and running without needing to run on my local machine
