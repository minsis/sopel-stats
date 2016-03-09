# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module
from .statsdb import *


def configure(config):
    pass


def setup(bot):
    pass

def current_count(_nick, _count_key):
    """ Returns the word count for a given nick"""

    try:
        word_count = int(bot.db.get_nick_value(_nick, _count_key))
    except:
        word_count = 0

    if word_count == None:
        word_count = 0

    return word_count

@module.require_chanmsg()
@module.commands("stats")
def print_stats(bot, trigger):
    """
    Print the stats to the channel it was called from. If no nick is given
    it will display your own stats
    """

    if not trigger.group(2):
        _nick = trigger.nick
    else:
        _nick = str(trigger.group(2)[0])

    _channel = str(trigger.sender)
    _count_key = "stats_wcount_" + _channel
    word_count = current_count(_nick, _count_key)

    bot.say("Stats for {} in {}".format(_nick, _channel))
    bot.say("Total Words: {}".format(word_count)

@module.require_chanmsg()
@module.rule("(.*)")
@module.priority("low")
def count_words(bot, trigger):
    """Counts the total words from a specific nick in a specific channel"""
    _nick = str(trigger.nick)
    _channel = str(trigger.sender)
    _message = str(trigger)
    _count_key = "stats_wcount_" + _channel

    bot.db.set_nick_value(_nick, "stats_timestamp_" + _channel, time.time())
    word_count = current_count(_nick, _count_key)
    bot.db.set_nick_value(_nick, _count_key, word_count += len(trigger))
