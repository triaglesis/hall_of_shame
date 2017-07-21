#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha', 'Dasha'

import vk
from time import strftime
import datetime

datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token=token)
# vkapi = vk.API(session)

curr_date = strftime("%d-%m-%Y")

from_typical_kirovohrad = "46631810"
from_scandal_kirovohrad = "80849532"

users_banned = vkapi('groups.getBanned',
                     count=50,
                     group_id=from_typical_kirovohrad)

# TODO:
# New version of users list extracting from api result
# This is not two dicts, it's now one list with index[0] = count of items
# users_banned.pop(0)

# Dive into the dict 'items' where user items are stored
users_banned = users_banned['items']

user_ban_id = ''
wiki_user_ban_id = ''
wiki_user_ban_comment = ''
wiki_user_banned_names = ''
users_banned_list = []
wiki_users_banned_list = []
wiki_table_start = "{| \n" \
                   "|- \n" \
                   "! Пользователь \n" \
                   "! Причина \n" \
                   "! Время Разбана:"
wiki_table_id = "\n|- \n" \
                "|"  # @id000000 \n
wiki_table_comment = "| "  # Comments, notes \n
wiki_table_date = "| "  # Date \n
wiki_table_end = "\n" \
                 "|}"

for user in users_banned:
    # Extract each user from dict and find for 'id' and 'comment' keys for each
    for comment in user:
        # Dive into the dict of 'items' where key is 'ban_info' and extract 'comment' and 'end_date'
        user_ban_info = user['ban_info']
        user_ban_comment = user_ban_info['comment']
        end_date = user_ban_info['end_date']
        # If date in not = '0
        if end_date:
            end_date = datetime.datetime.fromtimestamp(end_date).strftime('%Y-%m-%d; %H:%M:%S')
            end_date = str(end_date)
        else:
            end_date = "'''Никогда'''"
        # Dive into dict 'items' where key is 'id' for each user and convert int to string
        raw_user_ban_id = str(user['id'])
        # Extract user names
        raw_user_ban_first_name = str(user['first_name'])
        raw_user_ban_last_name = str(user['last_name'])
        for raw_id in raw_user_ban_id:
            # Add en extra symbols "@id" before each found user id and then add id and "SPACE" after it
            # Add for each id a construction of wiki-table tag
            user_ban_id = str("@id" + raw_user_ban_id + " ")
            # wiki_user_ban_id = str(wiki_table_id+ " @id" + raw_user_ban_id + " \n")
            # Splitting user names and last_names
            user_banned_names = raw_user_ban_first_name + " " + raw_user_ban_last_name
            # Making wiki-formatted string: new stroke<|->new stroke
            # <| @id000000>new stroke
            wiki_user_banned_names = wiki_table_id + user_banned_names + " \n"
            break
        # Composing string to wall like: <@id00000000> - <%user_ban_info['comment']%>new stroke
        # Composing next string to wiki like: <| %user_ban_comment%>new stroke
        # <| %end_date%>
        if user_ban_comment:
            ban_id_com = user_ban_id + "- " + user_ban_comment + "\n"
            wiki_user_ban_comment = str(wiki_table_comment + user_ban_comment + "\n" + wiki_table_date + end_date)
        else:
            ban_id_com = user_ban_id + "- " + "Без комментариев" + "\n"
            wiki_user_ban_comment = str(wiki_table_comment + "''Без комментариев'' \n" + wiki_table_date + end_date)
        wiki_ban_id_com = wiki_user_banned_names + wiki_user_ban_comment
        for each in ban_id_com:
            # Add each composed string to the list
            users_banned_list.append(ban_id_com)
            break
        for wiki_each in wiki_ban_id_com:
            # Add each composed string to the list for WIKI
            wiki_users_banned_list.append(wiki_ban_id_com)
            break
        break

# Add all found ids and comments with composed strings from list of it - to one string as text.
those_ids = ', '.join(users_banned_list)
all_ban = len(users_banned_list)
wiki_those_ids = ', '.join(wiki_users_banned_list)

those_ids_wall = those_ids.replace(',', '')
wiki_those_ids = wiki_those_ids.replace(',', '')

# Composing last tags of wiki table format:
# Example:
# {|
# |-
# ! Пользователь
# ! Причина
# ! Время Разбана:
# |-
# |Алина Головко
# | ''Без комментариев''
# | '''Никогда'''
# |}
wiki_ban_table = wiki_table_start + wiki_those_ids + wiki_table_end

message = "" \
    "Список забаненных пользователей в сообществе Типичный Кировоград: \n\nСписок сформирован: " + curr_date + "\n\n" \
    "Более подробная информация и дата разбана - в теме по ссылке внизу.\nПричины бана указаны для каждого участника " \
    "отдельно, для того чтобы вас убрали из этого списка - необходимо:\n - придерживаться правил сообщества \n " \
    " - придерживаться правил социальной сети Вконтакте \n - написать администратору с просьбой разбана и объяснением " \
    "причины того, что заставило вас нарушить наши правила \n\nДисклеймер:\nЗачем мы это делаем? Для того, чтобы " \
    "научить комьюнити - дисциплине и правилам поведения, не хотите попасть в список - не будьте хамлом, ботом, " \
    "рекламщиком, и все будет ок.\n\nЧтобы исчезнуть из этого списка, раз вы туда попали - надо раскаяться и больше " \
    "не повторять своих ошибок.\nДанный пост не преследует целей оскорбить или затравить пользователей, он создается " \
    "только для воспитательного момента, предотвращения нарушений и создания открытости между администрацией и " \
    "пользователями.\nТеперь никто просто так не попадет в бан потому, что не нравится админу, так как все участники " \
    "смогут быть адвокатами забаненного и могут помочь ему выйти по УДО.\n\n Внимание!\n Если вы оказались в этом " \
    "списке случайно, или не хотите в нем находиться, или вас это оскорбляет, задевает ваши чувства, то свяжитесь с " \
    "администрацией сообщества, мы исправим это недоразумение, и возможно, заменим причину бана на более лояльную.\n\n " \
    "#typical_kirovohrad, #ban_bot, #tk_ban_bot\n\n" \
    "\n\n #ВождьБот Powered by #Python made by #trianglesis\n\n"

ban_msg = "" \
    "== Список забаненных пользователей в сообществе Типичный Кировоград: == \n\nСписок сформирован: " + \
          curr_date + "\n\n" \
    "'''Более подробная информация и дата разбана - в теме по ссылке внизу.'''\nПричины бана указаны для каждого участника " \
    "отдельно, для того чтобы вас убрали из этого списка - необходимо:\n* придерживаться правил сообщества \n" \
    "* придерживаться правил социальной сети Вконтакте \n* написать администратору с просьбой разбана и объяснением " \
    "причины того, что заставило вас нарушить наши правила \n\n=== Дисклеймер: ===\nЗачем мы это делаем? Для того, чтобы " \
    "научить комьюнити - дисциплине и правилам поведения, не хотите попасть в список - не будьте хамлом, ботом, " \
    "рекламщиком, и все будет ок.\n\nЧтобы исчезнуть из этого списка, раз вы туда попали - надо раскаяться и больше " \
    "не повторять своих ошибок.\nДанный пост не преследует целей оскорбить или затравить пользователей, он создается " \
    "только для воспитательного момента, предотвращения нарушений и создания открытости между администрацией и " \
    "пользователями.\nТеперь никто просто так не попадет в бан потому, что не нравится админу, так как все участники " \
    "смогут быть адвокатами забаненного и могут помочь ему выйти по УДО.\n\n '''Внимание!\nЕсли вы оказались в этом " \
    "списке случайно, или не хотите в нем находиться, или вас это оскорбляет, задевает ваши чувства, то свяжитесь с " \
    "администрацией сообщества, мы исправим это недоразумение, и возможно, заменим причину бана на более лояльную.'''\n\n" \
    "\n\n #ВождьБот Powered by #Python made by #trianglesis\n\n"

# Adding message text plus wiki tags or ids ids to make wall post and wiki page
wall_message_text = (message + those_ids_wall)
wiki_message_text = (ban_msg + wiki_ban_table)

# Working groups
typical_kirovohrad = "-46631810"
scandal_kirovohrad = "-80849532"
typical_kirovohrad_boss = "13147598"

# Post the composed message to the wall:
wall_post = vkapi('wall.post',
                  owner_id=typical_kirovohrad,
                  from_group='1',
                  message=wall_message_text,
                  attachments='video13147598_171659721,'
                              'audio13147598_414979530,'
                              'page-46631810_49839429,',
                  signed='0')

# Post composed message to the wiki-page
user = '13147598'
# https://vk.com/typical_kirovohrad
group = '46631810'
# https://vk.com/page-46631810_49839429
page = '49839429'

wiki_page = vkapi.pages.save(text=wiki_message_text,
                             page_id=page,
                             group_id=group,
                             user_id=user,
                             title='')

print("Was found banned users and composed strings count:")
print(all_ban)
print("Message has been posted successfully!")