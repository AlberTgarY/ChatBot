import matplotlib.pyplot as plt
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication
from TextEditor import Readtxt

def sort(count_dict):
    temp_list = []
    key_list =[]
    for key in count_dict.keys():
        num = count_dict[key]
        if num <= 4:
            temp = {key: count_dict[key]}
            key_list.append(key)
            temp_list.append(temp)
    for key in key_list:
        count_dict.pop(key)
    return count_dict, temp_list

class Plot(object):


    @staticmethod
    def manipulate_data(output_dict):
        count_dict = {}
        # output_dict = {'anshumanbh-kubebot': [], 'brandonshin-slackbot-workout': [{'channels.list': "['channels:read']"}, {'channels.info': "['channels:read']"}, {'users.info': "['users:read']"}, {'users.get.Presence': []}], 'chakki-works-karura': [], 'DandyDev-slack-machine': [{'chat.post.Message': []}, {'chat.post.Ephemeral': []}, {'reactions.add': "['reactions:write']"}, {'conversations.list': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'conversations.info': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'im.close': "['im:write']"}, {'im.open': "['im:write']"}], 'haandol-honey': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'lins05-slackbot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'channels.history': "['channels:history']"}, {'im.history': "['im:history']"}, {'users.list': "['users:read']"}, {'rtm.start': "['client']"}, {'im.open': "['im:write']"}, {'users.get.Presence': []}, {'files.list': "['files:read']"}, {'channels.join': "['channels:write']"}, {'groups.list': "['groups:read']"}, {'channels.info': "['channels:read']"}, {'channels.invite': "['channels:write']"}, {'groups.invite': "['groups:write']"}, {'files.upload': '[]'}, {'reactions.add': "['reactions:write']"}], 'ogrodnek-code-pipeline-slack': [{'channels.list': "['channels:read']"}, {'channels.history': "['channels:history']"}, {'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}], 'rubenmak-PokemonGo-SlackBot': [], 'vitorverasm-slackbot-iot': [{'users.list': "['users:read']"}, {'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'brubakbd-XternSlackBot': [{'chat.post.Message': []}, {'users.list': "['users:read']"}, {'rtm.connect': "['client']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}], 'CaptainCuddleCube-igor': [], 'garr741-mr_meeseeks': [{'chat.post.Message': []}, {'channels.info': "['channels:read']"}, {'rtm.connect': "['client']"}, {'users.list': "['users:read']"}, {'users.info': "['users:read']"}, {'im.open': "['im:write']"}], 'jaipaddy-env-reserve-slackbot': [{'users.list': "['users:read']"}, {'rtm.connect': "['client']"}], 'jaklimoff-slack-sage': [{'rtm.start': "['client']"}, {'users.info': "['users:read']"}, {'channels.info': "['channels:read']"}, {'groups.info': "['groups:read']"}, {'chat.post.Message': []}], 'jerbly-medibot': [{'chat.post.Message': []}], 'jordan-simonovski-seefood-slackbot': [], 'jordanconway-slackbot-yubi': [{'rtm.connect': "['client']"}], 'kosyfrances-gitlab_mr_bot': [], 'aeranghang-slackbot': [], 'botiana-botiana': [{'rtm.connect': "['client']"}, {'files.upload': '[]'}, {'chat.post.Message': []}, {'chat.post.Ephemeral': []}, {'groups.set.Topic': []}, {'channels.set.Topic': []}, {'channels.info': "['channels:read']"}, {'users.info': "['users:read']"}, {'reactions.add': "['reactions:write']"}], 'chanshik-slack-timezone': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'api.test': '[]'}], 'hacklabkyiv-karmabot': [{'files.upload': '[]'}, {'channels.list': "['channels:read']"}, {'im.open': "['im:write']"}, {'reactions.get': "['reactions:read']"}, {'users.info': "['users:read']"}, {'rtm.connect': "['client']"}, {'channels.info': "['channels:read']"}, {'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}], 'hatwheels-parkio_slack_cmd': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'iSuperMostafa-pyslack-rtmbot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'auth.test': '[]'}], 'mike-wendt-redmine-slackbot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'users.info': "['users:read']"}, {'rtm.connect': "['client']"}], 'neefrehman-millzbot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}], 'nickweinberg-werewolf-slackbot': [{'rtm.connect': "['client']"}, {'channels.info': "['channels:read']"}, {'users.info': "['users:read']"}], 'asabot-slack_bot': [{'channels.info': "['channels:read']"}, {'users.info': "['users:read']"}, {'channels.history': "['channels:history']"}, {'chat.post.Message': []}], 'codepath-slackbot': [{'rtm.connect': "['client']"}, {'users.list': "['users:read']"}, {'users.profile.get': "['users.profile:read']"}], 'drunken-economist-dm-slack-bot': [], 'insynchq-slackbot': [{'users.list': "['users:read']"}, {'channels.list': "['channels:read']"}], 'jheloper-python-slackbot': [{'rtm.start': "['client']"}], 'LasVegasDataScience-slackbot': [{'rtm.connect': "['client']"}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'im.list': "['im:read']"}], 'rdcolema-gpt2-slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'servicemesher-slackbot': [], 'TRManderson-slackbot': [{'rtm.connect': "['client']"}], 'brenns10-groupme-slackbot': [], 'bticknor-tldr_slackbot': [{'rtm.connect': "['client']"}, {'im.history': "['im:history']"}, {'channels.history': "['channels:history']"}, {'chat.post.Message': []}], 'calc2te-python-slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'cloudpassage-don-bot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'files.upload': '[]'}, {'auth.test': '[]'}, {'groups.info': "['groups:read']"}, {'channels.info': "['channels:read']"}, {'im.list': "['im:read']"}, {'users.info': "['users:read']"}], 'ei-grad-vscale-slackbot': [], 'genebean-fbc-slackbot': [{'chat.post.Message': []}, {'conversations.history': "['channels:history', 'groups:history', 'im:history', 'mpim:history']"}], 'HugoDelval-flagbot': [{'channels.history': "['channels:history']"}, {'chat.post.Message': []}], 'marukosu-tasktracking-slackbot': [{'chat.post.Message': []}], 'Transport-Protocol-CADS_SLACKBOT': [{'users.list': "['users:read']"}, {'channels.list': "['channels:read']"}, {'rtm.connect': "['client']"}, {'chat.post.Message': []}], '99yen-slackbot-ojichat': [], 'CoffeeCodeAndCreatine-slackbot_real_time_messaging_api_example': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'gregmccoy-pyslackbot': [{'rtm.connect': "['client']"}], 'jgontrum-slackbot-uni-potsdam-cafeteria': [], 'OAODEV-remindbot': [{'users.info': "['users:read']"}], 'Rastii-SlackJira': [], 'rit-ai-ritai-bot': [], 'tomswartz07-SpaceLaunchSlackBot': [], 'Wsoren1-GoogleCalendar_to_Trello_Slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'CoaLee-hotword': [{'chat.post.Message': []}, {'files.upload': '[]'}, {'users.list': "['users:read']"}], 'flemingcaleb-InfraBot': [{'oauth.access': '[]'}, {'chat.post.Message': []}, {'chat.post.Ephemeral': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'conversations.info': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'users.info': "['users:read']"}], 'ianhillmedia-deletebot-for-slack-and-heroku': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'files.list': "['files:read']"}, {'files.delete': "['files:write', 'files:write:user']"}, {'rtm.connect': "['client']"}], 'jaredscottwilson-URLScanBot': [{'chat.post.Message': []}], 'netquity-err-fabric': [], 'RealmTeam-slack-sounds': [{'files.info': "['files:read']"}, {'users.list': "['users:read']"}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'chat.post.Ephemeral': []}], 'Solvik-gcp_status_to_slack': [], 'tmacro-archive-hitman-old': [{'oauth.token': '[]'}], '1kita-tanedy': [], 'akihanari-Slackbot': [], 'bmonty-aa5robot': [{'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'chat.post.Message': []}], 'irregularengineering-slackbot': [{'oauth.token': '[]'}], 'KoueiYamaoka-slackbot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}], 'litui-adhdbot-slack': [{'rtm.start': "['client']"}, {'channels.list': "['channels:read']"}, {'users.list': "['users:read']"}], 'loamhoof-slackbot': [{'rtm.connect': "['client']"}, {'users.list': "['users:read']"}, {'files.info': "['files:read']"}, {'reactions.add': "['reactions:write']"}], 'surevine-slackbot': [], 'tonythefreedom-slackbot': [{'oauth.token': '[]'}, {'team.info': "['team:read']"}, {'oauth.access': '[]'}, {'im.open': "['im:write']"}, {'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}], 'CoffeeCodeAndCreatine-slackbot_events_api_example': [{'chat.post.Message': []}], 'Galank-07-SLACKBOT': [{'groups.invite': "['groups:write']"}, {'im.list': "['im:read']"}, {'groups.list': "['groups:read']"}], 'hahahkim-slackbot': [], 'iMerica-safely': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'reactions.add': "['reactions:write']"}], 'jay-johnson-slack-driven-development': [{'chat.post.Message': []}], 'mozilla-netops-slackbot': [{'chat.post.Message': []}, {'conversations.set.Topic': []}, {'conversations.info': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'rtm.start': "['client']"}], 'sanjitjain2-Slackbot_build1': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'files.upload': '[]'}], 'sopitz-taigabot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'Watson-Personal-Assistant-simple_WA_slackbot': [{'auth.test': '[]'}, {'team.info': "['team:read']"}, {'chat.post.Message': []}, {'reactions.add': "['reactions:write']"}, {'files.upload': '[]'}, {'chat.post.Ephemeral': []}, {'conversations.history': "['channels:history', 'groups:history', 'im:history', 'mpim:history']"}, {'rtm.connect': "['client']"}], 'brianz-dilbert-slack-bot': [], 'ChaitanyaHaritash-SlackBot': [{'chat.post.Message': []}], 'CodeTheCity-slackbot-example': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'deadbits-slackbot-framework': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'files.upload': '[]'}, {'users.info': "['users:read']"}, {'users.list': "['users:read']"}, {'im.open': "['im:write']"}], 'DeepLab-deeplab_x_deepdream_slackbot': [{'files.list': "['files:read']"}], 'JasonQSY-nicebot': [{'chat.post.Message': []}], 'karl-run-haikubot': [{'rtm.connect': "['client']"}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'files.upload': '[]'}, {'channels.info': "['channels:read']"}], 'phospodka-slackhub': [{'chat.post.Message': []}, {'users.info': "['users:read']"}], 'yeahdef-lambdamagicbot': [], 'cpk42-xbrain-slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'gmontanola-trackco-slackbot': [], 'jyeeee95-jye_slackbot': [], 'keptn-sandbox-slackbot-service': [{'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}], 'MaayanLab-slackbot-tutorial': [{'chat.post.Message': []}], 'noahdabrowski-sae-slackbot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'primehaxor-devops-slackbot': [{'chat.post.Message': []}], 'SynapseFI-demo.slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'tommikarkas-cowsay-slackbot': [{'users.list': "['users:read']"}, {'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'askew1312-hogwarts': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'files.upload': '[]'}], 'fsalum-slackbot-python': [], 'lyft-omnibot': [], 'marvinpinto-charlesbot': [{'auth.test': '[]'}, {'rtm.connect': "['client']"}, {'users.info': "['users:read']"}], 'openfaas-cloud-functions': [], 'pyconjp-pyconjpbot': [{'users.info': "['users:read']"}, {'im.open': "['im:write']"}, {'users.list': "['users:read']"}, {'groups.list': "['groups:read']"}, {'channels.info': "['channels:read']"}, {'users.get.Presence': []}], 'thecarebot-carebot': [{'chat.post.Message': []}], 'thundergolfer-arXie-Bot': [{'chat.post.Message': []}], 'zbeaver4-python-webpage-monitor-slackbot': [{'rtm.connect': "['client']"}], 'DEADP0OL-DPoS-Slackbot': [{'im.open': "['im:write']"}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'eastend-street-translation_slackbot': [], 'inyukwo1-slackbot_boblabs_postech': [{'chat.post.Message': []}], 'moroleandro-aws-billing-slackbot': [], 'RachaelStannard-SlackBot-Mendel': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'Saurav-Shrivastav-Slackbot-tutorial': [{'chat.post.Message': []}], 'seymour1-baltimore-python-slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'Thakugan-blackjack-slackbot': [{'users.list': "['users:read']"}, {'channels.list': "['channels:read']"}, {'channels.create': "['channels:write']"}], 'YoungestSalon-SlackBot_Letter': [], 'Casualtek-Slackbot-for-Asterisk': [{'im.replies': "['im:history']"}, {'im.history': "['im:history']"}], 'DavidsonMachineLearningGroup-PainterBot': [{'files.upload': '[]'}, {'chat.post.Message': []}, {'users.info': "['users:read']"}], 'Denhac-LightWallSlackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'users.list': "['users:read']"}], 'jianshen92-slack-telegram-bot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'groups.info': "['groups:read']"}, {'channels.info': "['channels:read']"}, {'users.info': "['users:read']"}], 'KenzieAcademy-quackers': [{'oauth.access': '[]'}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'emoji.list': "['emoji:read']"}, {'chat.post.Ephemeral': []}, {'views.open': '[]'}, {'users.conversations': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}], 'marksansome-minecraft-uptime-slackbot': [{'chat.post.Message': []}], 'Nicoretti-sirtalkalot': [{'rtm.start': "['client']"}], 'r1d1-textNN': [], 'scottjlee-fidobot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'groups.info': "['groups:read']"}, {'reactions.get': "['reactions:read']"}, {'rtm.start': "['client']"}, {'files.upload': '[]'}, {'im.open': "['im:write']"}, {'reactions.add': "['reactions:write']"}], 'cloud-hackathon-slack-tetris': [{'users.list': "['users:read']"}, {'chat.post.Message': []}], 'Dominic-Kua-home_slack_runner': [{'rtm.connect': "['client']"}], 'dubirajara-slack-Bot': [{'chat.post.Message': []}, {'channels.history': "['channels:history']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}], 'dwyerk-slackers': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'ImShady-Tubey': [{'team.info': "['team:read']"}, {'oauth.token': '[]'}], 'jordan-simonovski-coffee-bot': [], 'Rycieos-slack-compilebot': [], 's-owl-ssslackbot': [], 'Srol-Slack-Horoscope-Bot': [], 'archydeberker-burnsbot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'users.list': "['users:read']"}], 'cybernetisk-slackbot': [], 'Deblob12-Nose-Goes': [], 'haandol-bee-bot': [{'chat.post.Message': []}], 'KenzieAcademy-se-q3-slackbot': [], 'meltaxa-slackmq': [{'pins.add': "['pins:write']"}, {'stars.add': '[]'}, {'reactions.add': "['reactions:write']"}, {'pins.remove': "['pins:write']"}, {'reactions.remove': "['reactions:write']"}, {'stars.remove': "['stars:write']"}], 'nejckorasa-slack-log-follower-bot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'sonanlee-Parroter': [], 'umentu-slackbot': [{'channels.list': "['channels:read']"}, {'chat.post.Message': []}], 'abij-car_lookup_slackbot': [{'oauth.token': '[]'}, {'team.info': "['team:read']"}, {'oauth.access': '[]'}, {'files.info': "['files:read']"}, {'chat.me.Message': []}, {'chat.post.Message': []}], 'ADI-Labs-slackbot-games': [{'channels.info': "['channels:read']"}, {'chat.post.Message': []}, {'channels.history': "['channels:history']"}], 'igorbragaia-slackbot': [], 'Mulgist-coinone-ticker-slackbot': [], 'NosKmc-nosponse': [{'chat.post.Message': []}, {'search.messages': "['search:read']"}, {'users.conversations': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'channels.list': "['channels:read']"}, {'users.list': "['users:read']"}, {'rtm.connect': "['client']"}], 'nycmeshnet-nycmeshbot': [], 'orez--SlackBot': [{'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'im.open': "['im:write']"}, {'im.close': "['im:write']"}, {'rtm.start': "['client']"}], 'whieronymus-slack-bot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'rtm.connect': "['client']"}, {'users.info': "['users:read']"}, {'channels.info': "['channels:read']"}], 'wooparadog-slackbot': [{'search.all': "['search:read']"}], 'gangstertim-orderAggregator': [], 'IBM-tririga-assistant-slackbot': [{'chat.post.Message': []}, {'users.info': "['users:read']"}, {'auth.test': '[]'}], 'jackreichelt-slackbot-tutorial': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'jy617lee-slackbot_datagirls': [], 'osmlab-osm-slackbot': [], 'sammous-SlackbotMention': [], 'sycs-climate-sycsbot': [{'oauth.token': '[]'}, {'chat.post.Message': []}, {'users.info': "['users:read']"}, {'rtm.start': "['client']"}], 'tym-xqo-oblique': [], 'xtream1101-slackbot-queue': [{'chat.post.Ephemeral': []}, {'reactions.add': "['reactions:write']"}, {'auth.test': '[]'}, {'rtm.connect': "['client']"}, {'conversations.history': "['channels:history', 'groups:history', 'im:history', 'mpim:history']"}, {'files.info': "['files:read']"}, {'chat.post.Message': []}, {'im.list': "['im:read']"}], 'AjithPanneerselvam-Slackbot': [], 'andrewsage-slackbot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'calebtote-slackbots': [{'rtm.connect': "['client']"}, {'channels.info': "['channels:read']"}, {'groups.info': "['groups:read']"}, {'chat.post.Message': []}, {'oauth.access': '[]'}, {'oauth.token': '[]'}, {'users.list': "['users:read']"}], 'claytantor-chatscript-slackbot4py': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'jeberl-slackbot': [], 'Resisty-slackbutt': [], 'rsalmond-slackbot': [], 'SaltyLeo-Slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'sophiecooper-stretchbot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], '085astatine-slackbot': [{'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'conversations.history': "['channels:history', 'groups:history', 'im:history', 'mpim:history']"}, {'team.info': "['team:read']"}, {'chat.post.Message': []}, {'auth.test': '[]'}, {'users.list': "['users:read']"}, {'conversations.list': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'conversations.info': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}], '98iamvaishu-slackbot': [{'chat.post.Message': []}], 'eloygbm-slackbot': [], 'itsdarshan-slackbot': [{'channels.info': "['channels:read']"}, {'chat.post.Message': []}], 'laddeos-slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'api.test': '[]'}, {'im.open': "['im:write']"}, {'im.history': "['im:history']"}], 'Nyzl-slackbot': [{'dialog.open': '[]'}, {'chat.post.Message': []}], 'singh1114-slackbot': [{'users.list': "['users:read']"}, {'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'Soundaryab12-slackbot': [{'chat.post.Message': []}, {'emoji.list': "['emoji:read']"}], 'tczorro-slackbot': [], 'aokabi-slackbot': [{'rtm.connect': "['client']"}, {'users.profile.set': "['users.profile:write']"}, {'users.set.Photo': []}], 'BRCentralSA-Slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'DiggerPlus-slackbot': [], 'jmcevoy1984-SlackBot': [{'api.test': '[]'}, {'chat.post.Message': []}], 'JSpiner-SlackBot': [{'rtm.connect': "['client']"}], 'nathants-slackbot': [], 'nshhhin-slackBot': [{'chat.post.Message': []}, {'reactions.add': "['reactions:write']"}, {'reactions.get': "['reactions:read']"}, {'chat.me.Message': []}, {'users.info': "['users:read']"}, {'usergroups.list': "['usergroups:read']"}, {'groups.list': "['groups:read']"}], 'rearyy-slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'vdfernandes-slackbot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'groups.list': "['groups:read']"}, {'users.info': "['users:read']"}, {'channels.info': "['channels:read']"}, {'groups.info': "['groups:read']"}, {'channels.history': "['channels:history']"}], 'AgalmicVentures-SlackBot': [], 'dingdongx2-slackbot_icewall': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'dstruthers-SlackBot': [], 'jonepl-SlackBot-Events-Api-Template': [{'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'dialog.open': '[]'}, {'files.upload': '[]'}, {'users.list': "['users:read']"}, {'im.history': "['im:history']"}, {'channels.list': "['channels:read']"}, {'channels.info': "['channels:read']"}, {'groups.info': "['groups:read']"}], 'kazmaw-SlackBot': [{'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'NihilisticRealist-SlackBot': [], 'sungjunyoung-SlackBot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'users.list': "['users:read']"}], 'VelazquezAJ-MargoBot': [{'api.test': '[]'}, {'users.info': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'rtm.start': "['client']"}], 'wqz9822-plant_bot': [{'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'im.history': "['im:history']"}, {'channels.history': "['channels:history']"}, {'reactions.add': "['reactions:write']"}], 'julianeon-slackbot': [{'chat.post.Message': []}, {'im.history': "['im:history']"}], 'nficano-slackcat': [], 'OperationCode-operationcode-pybot': [{'chat.post.Message': []}, {'users.info': "['users:read']"}, {'dialog.open': '[]'}, {'chat.post.Ephemeral': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'im.history': "['im:history']"}, {'conversations.invite': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'users.lookup.By.Email': []}, {'oauth.token': '[]'}], 'python-cn-flask-slackbot': [{'chat.post.Message': []}], 'savala-slackStocks': [], 'secdevopsai-Threat-Intel-Slack-Bot': [{'chat.post.Message': []}], 'ServerlessOpsIO-aws-sns-to-slack-publisher': [{'channels.list': "['channels:read']"}, {'chat.post.Message': []}], 'Techcatchers-Geeksters-Slack-Chatbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'UnitedIncome-slackbot-destroyer': [{'chat.post.Message': []}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'channels.list': "['channels:read']"}, {'channels.kick': "['channels:write']"}, {'rtm.connect': "['client']"}, {'users.list': "['users:read']"}], 'daxanya1-docker_slackbot': [{'chat.post.Message': []}], 'LisaUccini-nanoverde-bot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'macssmcgill-Atlas': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'mtane0412-ImaginaryCompanion': [], 'clamytoe-bdaybot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'users.info': "['users:read']"}, {'users.list': "['users:read']"}], 'cw75-torchMojiBot': [{'oauth.access': '[]'}, {'chat.post.Message': []}, {'oauth.v2.access': '[]'}, {'conversations.list': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'rtm.connect': "['client']"}, {'rtm.start': "['client']"}, {'admin.apps.approve': "['admin.apps:write']"}, {'admin.apps.requests.list': '[]'}, {'admin.apps.restrict': "['admin.apps:write']"}, {'admin.conversations.set.Teams': []}, {'admin.emoji.add': "['admin.teams:write']"}, {'admin.emoji.list': "['admin.teams:read']"}, {'emoji.list': "['emoji:read']"}, {'admin.emoji.remove': "['admin.teams:write']"}, {'admin.emoji.rename': "['admin.teams:write']"}, {'admin.users.session.reset': "['admin.users:write']"}, {'admin.invite.Requests.approve': []}, {'admin.invite.Requests.list': []}, {'admin.invite.Requests.deny': []}, {'admin.teams.admins.list': "['admin.teams:read']"}, {'admin.teams.create': "['admin.teams:write']"}, {'admin.teams.list': "['admin.teams:read']"}, {'admin.teams.settings.info': "['admin.teams:read']"}, {'admin.teams.settings.set.Default.Channels': []}, {'admin.teams.settings.set.Description': []}, {'admin.teams.settings.set.Discoverability': []}, {'admin.teams.settings.set.Icon': []}, {'admin.teams.settings.set.Name': []}, {'admin.usergroups.add.Channels': []}, {'admin.usergroups.list.Channels': []}, {'usergroups.list': "['usergroups:read']"}, {'groups.list': "['groups:read']"}, {'admin.usergroups.remove.Channels': []}, {'admin.users.assign': "['admin.users:write']"}, {'admin.users.invite': "['admin.users:write']"}, {'admin.users.list': "['admin.users:read']"}, {'users.list': "['users:read']"}, {'admin.users.remove': "['admin.users:write']"}, {'admin.users.set.Expiration': []}, {'admin.users.set.Owner': []}, {'admin.users.set.Regular': []}, {'api.test': '[]'}, {'auth.revoke': '[]'}, {'auth.test': '[]'}, {'bots.info': "['users:read']"}, {'calls.add': "['calls:write']"}, {'calls.end': "['calls:write']"}, {'calls.info': "['calls:read']"}, {'calls.participants.add': "['calls:write']"}, {'calls.update': "['calls:write']"}, {'channels.archive': "['channels:write']"}, {'channels.create': "['channels:write']"}, {'channels.history': "['channels:history']"}, {'channels.info': "['channels:read']"}, {'channels.invite': "['channels:write']"}, {'channels.join': "['channels:write']"}, {'channels.kick': "['channels:write']"}, {'channels.leave': "['channels:write']"}, {'channels.list': "['channels:read']"}, {'channels.mark': "['channels:write']"}, {'channels.rename': "['channels:write']"}, {'channels.replies': "['channels:history']"}, {'channels.set.Purpose': []}, {'channels.set.Topic': []}, {'channels.unarchive': "['channels:write']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'chat.schedule.Message': []}, {'chat.get.Permalink': []}, {'chat.post.Ephemeral': []}, {'chat.unfurl': "['links:write']"}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'conversations.archive': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.close': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.create': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.history': "['channels:history', 'groups:history', 'im:history', 'mpim:history']"}, {'conversations.info': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'conversations.invite': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.join': "['channels:write']"}, {'conversations.kick': '[]'}, {'conversations.leave': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.members': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'conversations.open': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.rename': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'conversations.replies': "['channels:history', 'groups:history', 'im:history', 'mpim:history']"}, {'conversations.set.Purpose': []}, {'conversations.set.Topic': []}, {'conversations.unarchive': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'dialog.open': '[]'}, {'dnd.end.Snooze': []}, {'dnd.info': "['dnd:read']"}, {'dnd.set.Snooze': []}, {'dnd.team.Info': []}, {'team.info': "['team:read']"}, {'files.comments.delete': "['files:write', 'files:write:user']"}, {'files.delete': "['files:write', 'files:write:user']"}, {'files.info': "['files:read']"}, {'files.list': "['files:read']"}, {'files.remote.info': "['remote_files:read']"}, {'files.remote.list': "['remote_files:read']"}, {'files.remote.add': '[]'}, {'files.remote.update': '[]'}, {'files.remote.remove': '[]'}, {'files.remote.share': "['remote_files:share']"}, {'files.revoke.Public.URL': []}, {'files.shared.Public.URL': []}, {'files.upload': '[]'}, {'groups.archive': "['groups:write']"}, {'groups.create': "['groups:write']"}, {'groups.history': "['groups:history']"}, {'groups.info': "['groups:read']"}, {'groups.invite': "['groups:write']"}, {'groups.kick': "['groups:write']"}, {'groups.leave': "['groups:write']"}, {'groups.mark': "['groups:write']"}, {'groups.open': "['groups:write']"}, {'groups.rename': "['groups:write']"}, {'groups.replies': "['groups:history']"}, {'groups.set.Purpose': []}, {'groups.set.Topic': []}, {'groups.unarchive': "['groups:write']"}, {'im.close': "['im:write']"}, {'im.history': "['im:history']"}, {'im.list': "['im:read']"}, {'im.mark': "['im:write']"}, {'im.open': "['im:write']"}, {'im.replies': "['im:history']"}, {'migration.exchange': '[]'}, {'mpim.close': "['mpim:write']"}, {'mpim.history': "['mpim:history']"}, {'mpim.list': "['mpim:read']"}, {'mpim.mark': "['mpim:write']"}, {'mpim.open': '[]'}, {'mpim.replies': "['mpim:history']"}, {'pins.add': "['pins:write']"}, {'pins.list': "['pins:read']"}, {'pins.remove': "['pins:write']"}, {'reactions.add': "['reactions:write']"}, {'reactions.get': "['reactions:read']"}, {'reactions.list': "['reactions:read']"}, {'reactions.remove': "['reactions:write']"}, {'reminders.add': "['reminders:write']"}, {'reminders.complete': "['reminders:write']"}, {'reminders.delete': "['reminders:write']"}, {'reminders.info': "['reminders:read']"}, {'reminders.list': "['reminders:read']"}, {'search.all': "['search:read']"}, {'search.files': "['search:read']"}, {'search.messages': "['search:read']"}, {'stars.add': '[]'}, {'stars.list': "['stars:read']"}, {'stars.remove': "['stars:write']"}, {'team.access.Logs': []}, {'team.billable.Info': []}, {'users.info': "['users:read']"}, {'team.integration.Logs': []}, {'team.profile.get': "['users.profile:read']"}, {'usergroups.create': "['usergroups:write']"}, {'usergroups.disable': "['usergroups:write']"}, {'usergroups.enable': "['usergroups:write']"}, {'usergroups.update': "['usergroups:write']"}, {'usergroups.users.list': "['usergroups:read']"}, {'usergroups.users.update': "['usergroups:write']"}, {'users.conversations': "['channels:read', 'groups:read', 'im:read', 'mpim:read']"}, {'users.delete.Photo': []}, {'users.get.Presence': []}, {'users.identity': "['identity.basic']"}, {'users.lookup.By.Email': []}, {'users.set.Photo': []}, {'users.set.Presence': []}, {'users.profile.get': "['users.profile:read']"}, {'users.profile.set': "['users.profile:write']"}, {'views.open': '[]'}, {'views.push': '[]'}, {'views.update': '[]'}, {'views.publish': '[]'}], 'epsagon-reddit-slackbot': [], 'jh69-commandlinefu_slackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'mwillsey-crossbot': [{'users.info': "['users:read']"}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'reactions.add': "['reactions:write']"}], 'rackerlabs-insightvm_slackbot': [{'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'users.info': "['users:read']"}, {'chat.post.Message': []}], 'ryanohoro-slack-metabot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'sinramyeon-old_ver_bot': [{'chat.post.Message': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}, {'oauth.access': '[]'}], 'vishwa35-slackbot-tutorial': [{'chat.post.Message': []}], 'harshibar-conga-slackbot': [], 'jroyal-IDS-Slackbot': [], 'kvarga-slackbotjira': [], 'NosajGithub-stock-quote-slackbot': [{'rtm.connect': "['client']"}], 'oneor0-blockkit-slack': [], 'sedders123-phial': [{'chat.post.Ephemeral': []}, {'reactions.add': "['reactions:write']"}, {'files.upload': '[]'}, {'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'Tmw-edward': [{'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'files.upload': '[]'}], 'wagase-pokeshiri': [], 'depromeet-slackbot': [], 'ecapuano-slackbot': [], 'eda3-pyconjp2020-slackbot': [], 'nanflasted-TekinBot': [], 'newsdev-nyt-campfinbot': [{'rtm.connect': "['client']"}], 'newsdev-nyt-scotusbot': [{'rtm.connect': "['client']"}], 'odanado-slackbot-os-command-injection': [{'auth.test': '[]'}], 'Parsely-slackbot': [], 'pybites-slackbot': [{'channels.list': "['channels:read']"}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'convisoappsec-mitreattackbot': [{'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'auth.test': '[]'}], 'DankCity-dankbot': [{'chat.post.Message': []}], 'Denton-L-lavid-du': [{'users.list': "['users:read']"}, {'auth.test': '[]'}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}], 'ianhillmedia-slackbot-for-heroku': [{'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'chat.post.Message': []}], 'jperezlatimes-tyranobot': [{'rtm.connect': "['client']"}, {'chat.post.Message': []}], 'rudeigerc-scrapy-slackbot': [{'chat.post.Message': []}], 'shuichi-ochiai-MrSearch': [], 't-davidson-piazza-slackbot': [{'chat.post.Message': []}], 'yymao-slackbots': [], 'ASU-CodeDevils-flameboi-slack-api': [{'views.publish': '[]'}, {'views.update': '[]'}, {'chat.post.Message': []}, {'reactions.add': "['reactions:write']"}, {'channels.invite': "['channels:write']"}, {'users.lookup.By.Email': []}, {'users.info': "['users:read']"}, {'users.list': "['users:read']"}, {'channels.list': "['channels:read']"}, {'chat.post.Ephemeral': []}, {'conversations.open': "['channels:write', 'groups:write', 'im:write', 'mpim:write']"}, {'reactions.get': "['reactions:read']"}, {'reactions.remove': "['reactions:write']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}], 'bluscreenofjeff-SlackBots': [], 'dennyzhang-chatops_slack': [], 'devchat-dev-devolio-slackbot': [{'im.open': "['im:write']"}, {'chat.me.Message': []}, {'channels.list': "['channels:read']"}], 'hattan-kairo': [{'auth.test': '[]'}, {'rtm.connect': "['client']"}, {'chat.post.Message': []}, {'users.list': "['users:read']"}], 'pyasi-crypto-bot': [{'oauth.access': '[]'}, {'chat.post.Message': []}, {'chat.post.Ephemeral': []}, {'chat.update': "['chat:write', 'chat:write:bot', 'chat:write:user']"}], 'susumuishigami-maidchan-slackbot': [], 'TheKevJames-jarvis': [{'rtm.connect': "['client']"}, {'auth.test': '[]'}, {'users.list': "['users:read']"}, {'im.open': "['im:write']"}, {'chat.post.Message': []}, {'files.upload': '[]'}], 'wen830722-SlackBot-Simplest-Tutorial': [{'chat.post.Message': []}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'im.list': "['im:read']"}, {'users.info': "['users:read']"}, {'channels.info': "['channels:read']"}, {'oauth.token': '[]'}, {'team.info': "['team:read']"}, {'oauth.access': '[]'}], 'blattus-lombardi': [{'emoji.list': "['emoji:read']"}], 'jhwhite-reddit-slackbot': [{'chat.post.Message': []}], 'jonluca-Textbookbot': [], 'KyberNetwork-slackbot': [{'rtm.connect': "['client']"}, {'channels.kick': "['channels:write']"}, {'chat.post.Ephemeral': []}, {'users.info': "['users:read']"}, {'chat.delete': "['chat:write', 'chat:write:user', 'chat:write:bot']"}, {'files.delete': "['files:write', 'files:write:user']"}, {'pins.add': "['pins:write']"}, {'pins.remove': "['pins:write']"}, {'channels.list': "['channels:read']"}, {'channels.set.Topic': []}, {'channels.set.Purpose': []}, {'users.list': "['users:read']"}, {'chat.post.Message': []}, {'reminders.add': "['reminders:write']"}], 'mk200789-hello_slackbot': [{'oauth.access': '[]'}, {'chat.post.Message': []}, {'rtm.connect': "['client']"}, {'users.list': "['users:read']"}], 'orangespaceman-awkbot-slack': [{'rtm.connect': "['client']"}], 'py-suruga-py-suruga-13-slackbot-handson': [], 'supistar-Botnyan': [], 'thebotguys-poloniex-graph-chart-bot': [{'chat.post.Message': []}, {'rtm.start': "['client']"}, {'im.open': "['im:write']"}]}
        for key in output_dict.keys():
            for branch in output_dict[key]:
                for method in branch.keys():
                    if not method in count_dict.keys():
                        temp_dict = {method: 1}
                        count_dict.update(temp_dict)
                    else:
                        count_dict[method] = count_dict[method] + 1
        # print(count_dict)
        return count_dict
    @staticmethod
    def plot(count_dict):
        count_dict, temp_dict = sort(count_dict)
        print(temp_dict)

        # Bar plot
        plt.figure(figsize=(50, 10), dpi=80)
        N = len(count_dict)
        values = sorted(list(count_dict.values()), reverse=True)
        index = np.arange(N)
        width = 0.3
        p2 = plt.bar(index, values, width, label="occur times", color="#87CEFA")
        plt.xlabel('method')
        plt.ylabel('number of appearance')
        plt.title('Frequency of method')
        plt.xticks(index ,list(count_dict.keys()), rotation= 60)
        plt.legend(loc="upper right")
        plt.show()