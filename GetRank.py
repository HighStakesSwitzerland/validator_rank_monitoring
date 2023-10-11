#!/usr/bin/python3
from time import sleep
from requests import get
from discord import SyncWebhook, Embed

from validators import *

class GetRank:
    def __init__(self):
        super().__init__()
        self.discord_url = 'DISCORD WEBHOOK HERE' #(right click on your discord channel --> Edit Channel --> Integrations --> create a webhook and paste its url here)
        self.first_run = True #avoid sending discord alerts each time the process is restarted

    def run(self):
        """query the api for the validator set, get total and our rank.
        This requires the valcons address, which can be retrieved with : 'gaiad tendermint show-address' for example

        It's a little clumsy because this version is standalone and does not store the data anywhere.

        Run with "nohup python3 GetRank.py &", for example."""

        while True:

            for validator in validators:
                rank, total = self.query(validator) #get the current position and the length of the active set

                validator[5] = total #update the active set. Shouldn't change but sometimes it's not filled, e.g. Shentu, so there may be some movement.
                if rank != validator[4] and not self.first_run:
                    diff = validator[4] - rank

                    if not diff == 0: #no change, do nothing.
                        if rank == 0:
                            color = 00000000 #black
                            description = f"{validator[0]} has left the active set!"
                        elif diff < 0:
                            color = 16515843 #red
                            description = f"{validator[0]} moved down {abs(diff)} position(s).\nIt is currently {rank}/{total}."
                        elif diff > 0:
                            color = 2161667 #green
                            if validator[4] == 0:
                                description = f"{validator[0]} entered the active set at position {diff}/{total}"
                            else:
                                description = f"{validator[0]} moved up {diff} position(s).\nIt is currently {rank}/{total}"

                        validator[4] = rank #update the value in the list

                        self.discord_message(color,description)

                if self.first_run:
                    validator[4] = rank  # update the value in the list
                print(validator)

            if self.first_run:
                self.first_run = False #next run there can be alerts upon changes

            sleep(120) #check this every couple minutes

    def query(self, validator):
        url = f"http://{validator[1]}:{validator[2]}/cosmos/base/tendermint/v1beta1/validatorsets/latest?pagination.offset="
        i = 0
        valset = []
        attempt = 0
        while True:
            try:
                results = get(url + str(i), timeout=5).json()
                # print(len(results['validators']))
                valset += results['validators']
                i += 100
                sleep(1)
            except KeyError:  # no such key --> end of pages
                break
            except Exception as e:
                if attempt < 3:
                    attempt += 1  #REST server did not respond ? Wait a bit and retry
                    sleep(5)
                else: #abort
                    print(f"ERROR for {validator[0]}. Please check configuration: {e}")
                    return validator[4],validator[5]
        # get index of our validator in the list
        try:
            index = [valset.index(i) for i in valset if i['address'] == validator[3]][0] + 1  # indexes start at 0, list at 1
        except Exception as e:  # valcons not present in the valset... validator either jailed or out of the active set.
            index = 0
        total = len(valset)

        return index, total

    def discord_message(self, color, description):
        webhook = SyncWebhook.from_url(self.discord_url)
        embed = Embed(title="Rank Alert", description=description, color=color)
        webhook.send("<@user_id_1> <@user_id_2>", embed=embed)

        #discord messages can tag specific users identified by their user_id (right click on a user name, --> Copy User ID).
        #mind the syntax : enclose the id between < >, don't omit the @.
        #no comma between multiple users.

GetRank().run()