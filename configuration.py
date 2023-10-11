#the discord channel where the alerts will be sent
discord_url = 'DISCORD WEBHOOK HERE' #(right click on your discord channel --> Edit Channel --> Integrations --> create a webhook and paste its url here)
#it looks like : https://discord.com/api/webhooks/973931341296440724/y5nDXqVJUNfKx27BBh6LeN5tCTQLEHtOcF_JXZexnfZKh55i0J1LXbmeBGuFv3nmICvV

#discord messages can tag specific users identified by their user_id (right click on a user name, --> Copy User ID).
#mind the syntax : enclose the id between < >, don't omit the @.
#no comma between multiple users.
#leave empty if you don't want to tag anyone.
tagged_users = "" #example : "<@123456982335746> <@4568796543321654>"

#details of the different validators to monitor -- name, ip, api port, and consensus address
#last two items in the lists will store the current position, and the size of the active set
#Mind the structure of the data : a list of lists

validators = [
    ['FETCHAI', 'SERVER_IP', 'API_PORT', 'fetchvalcons1xxxxx', 0, 0],
    ['PERSISTENCE', 'SERVER_IP', 'API_PORT', 'persistencevalcons1xxxx', 0, 0],
    ['SHENTU', 'SERVER_IP', 'API_PORT', 'shentuvalcons1xxx', 0, 0]
]