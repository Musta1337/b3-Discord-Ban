

__author__ = 'Musta'
__version__ = '1.0'

import b3
import b3.plugin
import b3.events
import datetime
import urllib2
import json
from b3.functions import minutesStr


class DiscordbanPlugin(b3.plugin.Plugin):

    def __init__(self, console, config=None):
        """
        Build the plugin object.
        :param console: The parser instance.
        :param config: The plugin configuration object instance.
        """
        #########Checking if Admin Plugin is enabled.#########
        b3.plugin.Plugin.__init__(self, console, config)
        self.adminPlugin = self.console.getPlugin('admin')
        if not self.adminPlugin:
            raise AttributeError('could not start without admin plugin')
        ######################################################

    def onLoadConfig(self):
        """
        Load plugin configuration.
        """
        ##Loading data from conf file.##
        self._discordWebhookUrl = self.config.get('data','webhookUrl')
        self._serverName = self.config.get('data','hostname')
        self._b3Version = self.config.get('data','b3Version')
        self._clanName = self.config.get('data','clanName')
        self._clanWebsite = self.config.get ('data','clanWebsite')
        self._clanIcon = self.config.get ('data','clanIcon')
        self._clanBanAppeal = self.config.get ('data','clanBanAppeal')
        #Image below at the plugin startup
        self._clanHeader = self.config.get ('data','clanHeader')
        ################################
    def onStartup(self):
        """
        Initialize plugin settings.
        """

        ########Getting Events from b3 and Assigning to an ID.###########
        self.registerEvent(self.console.getEventID('EVT_CLIENT_BAN'), self.onBan)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_BAN_TEMP'), self.onBan)
        self.registerEvent(self.console.getEventID('EVT_CLIENT_KICK'), self.onKick)
        ##################################################################

        ##Logging at Plugin Start.##
        self.debug('plugin started')

        ##Pushing Embed message on plugin startup##
        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Ban Report",
            "url": self._clanWebsite,
            "description": "Big Brother Bot ban report plugin Succesfully loaded.",
            "timestamp": datetime.datetime.now().isoformat(),
            "color": 3093151,
            "image": {
                    "url": self._clanHeader
            },
            "thumbnail": {
                    "url": self._clanIcon
            },
            "fields": [

                {
                    "name": "Connected Server",
                    "value": '%s' % (self._serverName),
                    "inline": False
                },
                {
                    "name": "B3 Version",
                    "value": '%s' % (self._b3Version),
                    "inline": False
                },
                {
                    "name": "Credit",
                    "value": "**Ban Report v1.0 by Musta#6735**",
                    "inline": False
                },
                {
                    "name": "Unfair Ban?",
                    "value": "If you are banned unfairly by our administrator in official clan server, please make a ban appeal [here](%s)" % (self._clanBanAppeal),
                    "inline": False
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._clanName
            }
        }

        self.discordEmbeddedPush(embed)
        #######################################
    def onBan(self, event):
        """
        Perform operations when EVT_CLIENT_BAN or EVT_CLIENT_BAN_TEMP is received.
        :param event: An EVT_CLIENT_BAN or and EVT_CLIENT_BAN_TEMP event.
        """
        ##Getting the even contestants on the line and giving them new name.##
        admin = event.data['admin']
        client = event.client
        reason = event.data['reason']
        ######################################################################
        ##Beautiful Ban message for Beautiful People.##
        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Client Ban",
            "description": '**%s** Banned **%s**' % (admin.name, client.name),
            "timestamp": datetime.datetime.now().isoformat(),
            "thumbnail": {
                    "url": self._clanIcon
            },
            "color": 3093151,
            "fields": [
                {
                    "name": "Server",
                    "value": self._serverName,
                    "inline": False
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._serverName
            }
        }
        #################################################
        ##AKA If Admin is good who banned##
        if reason:
            embed["fields"].append({
                "name": "Reason for Ban",
                "value": self.console.stripColors(reason),
                "inline": True
            })
        ##RIP Permanent Ban##
        duration = 'permanent'
        if 'duration' in event.data:
        ##This line is little fishy but Got it working.##
            duration = minutesStr(event.data['duration'])
        #################################################
        embed["fields"].append({
                "name": "Duration of Ban",
                "value": duration,
                "inline": True
				})
        ##Pushing message##
        self.discordEmbeddedPush(embed)

    def onKick(self, event):
        """
        Perform operations when EVT_CLIENT_KICK is received.
        :param event: An EVT_CLIENT_KICK event.
        """
        ##Getting Sub event contestants##
        admin = event.data['admin']
        client = event.client
        reason = event.data['reason']
        #################################
        
        ##Beautiful Kick Message for Beautiful People##
        embed = {
            "author": {
                   "name": self._clanName,
                   "icon_url": self._clanIcon
            },
            "title": "Client kick",
            "description": '**%s** Kicked **%s**' % (admin.name, client.name),
            "timestamp": datetime.datetime.now().isoformat(),
            "thumbnail": {
                    "url": self._clanIcon
            },
            "color": 3093151,
            "fields": [
                {
                    "name": "Server",
                    "value": self._serverName,
                    "inline": False
                }
            ],
            "footer": {
                    "icon_url": self._clanIcon,
                    "text": self._serverName
            }
        }
        ###############################################


        ##AKA If Admin is good who kicked##
        if reason:
            embed["fields"].append({
                "name": "Reason for Kick",
                "value": self.console.stripColors(reason),
                "inline": True
            })
        #pushing message
        self.discordEmbeddedPush(embed)
    #### Copied from my last report Plugin :/####
    def discordEmbeddedPush(self, embed):
        """
        Embed Message push code from stack overflow
        """
        data = json.dumps({"embeds": [embed]})
        req = urllib2.Request(self._discordWebhookUrl, data, {'Content-Type': 'application/json',
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36"
        })

        try:
            urllib2.urlopen(req)
        except urllib2.HTTPError as ex:
            self.debug("Check Webhook link.")
            self.debug("Data: %s\nCode: %s\nRead: %s" % (data, ex.code, ex.read()))
    ###THE END##