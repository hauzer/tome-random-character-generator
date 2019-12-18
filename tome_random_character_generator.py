import json
import requests
import sys

class Campaign:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

campaigns = [
    Campaign("Maj'Eyal: The Age of Ascendancy"),
    Campaign('Orcs: Embers of Rage'),
    # Campaign('Infinite Dungeon: The Neverending Descent'),
    # Campaign('The Arena: Challenge of the Master')
]

class MetaRace:
    def __init__(self, name, races):
        self.name = name
        self.races = races
        for race in self.races:
            race.metarace = self

    def __str__(self):
        return '{}: {}'.format(self.name, ''.join('{},'.format(race) for race in self.races))

class Race:
    def __init__(self, name, metarace=None, disallowed_campaigns=None):
        self.name = name
        self.metarace = metarace
        if disallowed_campaigns:
            self.disallowed_campaigns = disallowed_campaigns
        else:
            self.disallowed_campaigns = []

    def __str__(self):
        return self.name

metaraces = [
    MetaRace('Human', [
        Race('Cornac', disallowed_campaigns=[campaigns[1]]),
        Race('Higher', disallowed_campaigns=[campaigns[1]])
    ]),
    MetaRace('Elf', [
        Race('Shalore', disallowed_campaigns=[campaigns[1]]),
        Race('Thalore', disallowed_campaigns=[campaigns[1]]),
        Race('Doomelf', disallowed_campaigns=[campaigns[1]])
    ]),
    MetaRace('Halfling', [
        Race('Halfling', disallowed_campaigns=[campaigns[1]])
    ]),
    MetaRace('Dwarf', [
        Race('Dwarf', disallowed_campaigns=[campaigns[1]]),
        Race('Drem', disallowed_campaigns=[campaigns[1]])
    ]),
    MetaRace('Yeek', [
        Race('Yeek', disallowed_campaigns=[campaigns[1]])
    ]),
    MetaRace('Giant', [
        Race('Ogre', disallowed_campaigns=[campaigns[1]]),
        Race('Krog', disallowed_campaigns=[campaigns[1]])
    ]),
    MetaRace('Undead', [
        Race('Ghoul', disallowed_campaigns=[campaigns[1]]),
        Race('Skeleton', disallowed_campaigns=[campaigns[1]]),
        Race('Whitehoof', disallowed_campaigns=[campaigns[0]])
    ]),
    MetaRace('Orc', [
        Race('Orc', disallowed_campaigns=[campaigns[0]])
    ]),
    MetaRace('Yeti', [
        Race('Kruk Yeti', disallowed_campaigns=[campaigns[0]])
    ])
]

class MetaClass:
    def __init__(self, name, classes):
        self.name = name
        self.classes = classes
        for class_ in self.classes:
            class_.metaclass = self

    def __str__(self):
        return '{}: {}'.format(self.name, ''.join('{},'.format(class_) for class_ in self.classes))

class Class:
    def __init__(self, name, metaclass=None, limited_to_races=None, disallowed_races=None):
        self.name = name
        self.metaclass = metaclass
        if limited_to_races:
            self.limited_to_races = limited_to_races
        else:
            self.limited_to_races = []
        if disallowed_races:
            self.disallowed_races = disallowed_races
        else:
            self.disallowed_races = []

    def __str__(self):
        return self.name

metaclasses = [
    MetaClass('Warrior', [
        Class('Berserker'),
        Class('Bulwark'),
        Class('Archer'),
        Class('Arcane Blade'),
        Class('Brawler')
    ]),
    MetaClass('Rogue', [
        Class('Rogue'),
        Class('Shadowblade'),
        Class('Marauder'),
        Class('Skirmisher')
    ]),
    MetaClass('Mage', [
        Class('Alchemist'),
        Class('Archmage'),
        Class('Necromancer')
    ]),
    MetaClass('Wilder', [
        Class('Summoner', disallowed_races=metaraces[6].races),
        Class('Wyrmic', disallowed_races=metaraces[6].races),
        Class('Oozemancer', disallowed_races=metaraces[6].races),
        Class('Stone Warden', limited_to_races=metaraces[3].races)
    ]),
    MetaClass('Celestial', [
        Class('Sun Paladin'),
        Class('Anorithil')
    ]),
    MetaClass('Defiler', [
        Class('Reaver'),
        Class('Corruptor'),
        Class('Doombringer'),
        Class('Demonologist')
    ]),
    MetaClass('Afflicted', [
        Class('Cursed'),
        Class('Doomed')
    ]),
    MetaClass('Chronomancer', [
        Class('Paradox Mage'),
        Class('Temporal Warden')
    ]),
    MetaClass('Psionic', [
        Class('Mind Slayer'),
        Class('Solipsist'),
        Class('Possessor')
    ]),
    MetaClass('Adventurer', [
        Class('Adventurer')
    ]),
    MetaClass('Demented', [
        Class('Writhing One'),
        Class('Cultist of Entropy')
    ]),
    MetaClass('Tinker', [
        Class('Sawbutcher'),
        Class('Gunslinger'),
        Class('Psyshot'),
        Class('Annihilator')
    ])
]

class RandomOrgClient:
    URL = 'https://api.random.org/json-rpc/2/invoke'
    BASE_PAYLOAD = {
        'jsonrpc': '2.0',
        'id': 0
    }

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_payload = {
            **self.BASE_PAYLOAD,
            'params': {
                'apiKey': api_key
            }
        }

    def request(self, method, **kwargs):
        payload = {
            **self.base_payload,
            'method': method,
        }
        payload['params'].update(kwargs)

        return requests.post(self.URL, data=json.dumps(payload), headers={'content-type': 'application/json'}).json()['result']['random']['data']

def main():
    if len(sys.argv) > 1 and sys.argv[1].lower() == '--eor':
        allowed_campaigns = [campaigns[1]]
    else:
        allowed_campaigns = campaigns

    classes = [class_ for metaclass in metaclasses for class_ in metaclass.classes]
    races = [race for metarace in metaraces for race in metarace.races if len([campaign for campaign in allowed_campaigns if campaign not in race.disallowed_campaigns]) > 0]

    max_metarace_size = 0
    for metarace in metaraces:
        metarace_size = len(metarace.races)
        if metarace_size > max_metarace_size:
            max_metarace_size = metarace_size

    client = RandomOrgClient('da09e251-22ec-4187-ae9b-b8364c78cc89')
    if len(allowed_campaigns) > 1:
        data = client.request(
            'generateIntegerSequences',
            n=4,
            length=[1, 3, max_metarace_size, 2],
            min=[0, 0, 0, 0],
            max=[
                len(classes) - 1,
                len(races) - 1,
                max_metarace_size - 1,
                len(allowed_campaigns) - 1
            ],
            replacement=[True, False, False, False]
        )
    else:
        data = client.request(
            'generateIntegerSequences',
            n=3,
            length=[1, 3, max_metarace_size],
            min=[0, 0, 0],
            max=[
                len(classes) - 1,
                len(races) - 1,
                max_metarace_size - 1
            ],
            replacement=[True, False, False]
        )

    class_ = classes[data[0][0]]
    if class_.limited_to_races:
        for race_index in data[2]:
            try:
                race = class_.limited_to_races[race_index]
            except IndexError:
                continue
            break
    elif class_.disallowed_races:
        for race_index in data[1]:
            race = races[race_index]
            if race not in class_.disallowed_races:
                break
    else:
        race = races[data[1][0]]

    if len(allowed_campaigns) > 1:
        if race.disallowed_campaigns:
            for campaign_index in data[3]:
                campaign = allowed_campaigns[campaign_index]
                if campaign not in race.disallowed_campaigns:
                    break
        else:
            campaign = allowed_campaigns[data[3][0]]
    else:
        campaign = allowed_campaigns[0]

    print('{}\n{} {}'.format(campaign, race, class_))

if __name__ == '__main__':
    main()
