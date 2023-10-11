***Monitor the position of a validator in the active set of any Cosmos blockchain, and get alerted on Discord upon a change.***

This requires querying a node API and uses the consensus address, as well as the webhook for a Discord channel.

The code is mostly a skeleton with minimal functionality and can be improved in many ways -- threading, database, etc.

**Requirements**
Required packages should be present by default (time, requests) except Discord, which can be installed with <code>pip install discord</code>

**Usage**

Fill out the items in <b>configuration.py</b>. Make sure to follow the instructions.

Note: older versions of the Discord package require the webhook url to be enclosed in brackets. If you run into an error, you can try to update the file like `discord_url = ['your_webhook']`.

Run for example with `nohup python3 GetRank.py &`, or through a service.
