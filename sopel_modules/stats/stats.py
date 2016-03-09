# coding=utf-8
"""
stats.py - Advanced stats module for Sopel IRC bot.
Author: Dennis Whitney
Handle: minsis
Email: dwhitney@irunasroot.com

Copyright © 2016, Dennis Whitney <dwhitney@irunasroot.com>
Licensed under the Eiffel Forum License 2.
"""

from __future__ import unicode_literals, absolute_import, division, print_function

from sopel import module

#import time

def configure(config):
    pass


def setup(bot):
    pass

def get_local_word_count(bot, _nick, _count_key):
    """ Returns the word count for a given nick for the specific channel"""

    try:
        word_count = int(bot.db.get_nick_value(_nick, _count_key))
    except:
        word_count = 0

    return word_count

def get_global_word_count(bot, _nick):
    """Returns the global word count for a given nick"""

    nick_id = str(bot.db.get_nick_id(_nick, False))
    if nick_id is not None:
        sql_query_wcount = ("SELECT SUM(CAST(value AS INTEGER)) FROM nick_values WHERE "
                           "nick_id = ? AND "
                           "key like 'stats_wcount_%';")
        word_count = bot.db.execute(sql_query_wcount, (nick_id,)).fetchone()[0]

        if word_count is None: word_count = 0
    else:
        word_count = 0

    return word_count

def get_nick(bot, trigger):
    """Get the nick of stats to lookup"""

    if not trigger.group(2) or trigger.group(2) == trigger.nick:
        _nick = trigger.nick
        count_words(bot, trigger)
    else:
        _nick = str(trigger.group(2))

    return _nick

@module.thread(False)
@module.require_chanmsg()
@module.rule("(.*)")
@module.priority("low")
def count_words(bot, trigger):
    """Counts the total words from a specific nick in a specific channel"""

    _nick = str(trigger.nick)
    _channel = str(trigger.sender)
    _message = str(trigger)
    _count_key = "stats_wcount_" + _channel

    word_count = get_local_word_count(bot, _nick, _count_key) + len(trigger.split())
    bot.db.set_nick_value(_nick, _count_key, word_count)

@module.require_chanmsg()
@module.commands("words")
def print_words(bot, trigger):
    """Print the word count for a given nick for the channel it was called from. If no nick is given it will display your own word count"""

    _nick = get_nick(bot,trigger)
    _channel = str(trigger.sender)
    _count_key = "stats_wcount_" + _channel
    word_count = get_local_word_count(bot, _nick, _count_key)

    bot.say("Total words for {} in {}: ".format(_nick, _channel, word_count))

@module.require_chanmsg()
@module.commands("gwords")
def print_gwords(bot, trigger):
    """Print the global word count for a given nick. If no nick is given it will display your own word count"""

    _nick = get_nick(bot,trigger)
    word_count = get_global_word_count(bot, _nick)

    bot.say("Total words for {} in all channels: {}".format(_nick, word_count))

@module.require_chanmsg()
@module.commands("stats")
def print_stats(bot, trigger):
    """Print the stats for a given nick for the channel it was called from. If no nick is given it will display your own stats."""

    _nick = get_nick(bot,trigger)
    _channel = str(trigger.sender)
    _count_key = "stats_wcount_" + _channel
    word_count = get_local_word_count(bot, _nick, _count_key)

    bot.say("Stats for {} in {}".format(_nick, _channel))
    bot.say("Total Words: {}".format(word_count))

@module.require_chanmsg()
@module.commands("gstats")
def print_gstats(bot, trigger):
    """Print the global stats for a nick. If no nick is given it will display your own stats."""

    _nick = get_nick(bot,trigger)
    word_count = get_global_word_count(bot, _nick)

    bot.say("Stats for {} globally".format(_nick))
    bot.say("Total Words: {}".format(word_count))
