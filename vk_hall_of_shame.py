#! /usr/bin/env python3
# coding=utf-8
__author__ = 'Dasha', 'danilcha'
# Change history
# 2015-11-24 Add note about new API method after VK_module update, and new list parsing method.
# 2015-11-24 Add env details and encode

import vk

# TODO:
# New version for Vkontakte api for module ver 2.0a4 and above
token = 'TOKEN'
# session = vk.Session(access_token=token)
vkapi = vk.API(access_token = token)
# vkapi = vk.API(session)

from_typical_kirovohrad = "46631810"
from_scandal_kirovohrad = "80849532"

users_banned = vkapi('groups.getBanned',
                     count=100,
                     group_id=from_scandal_kirovohrad)

users_banned = users_banned['items']

# TODO:
# New version of users list extracting from api result
# This is not two dicts, it's now one list with index[0] = count of items
# users_banned.pop(0)

users_ids = []
for user in users_banned:
    for some in user:
        user_int = user['id']
        user_str = str(user_int)
        for raw_id in user_str:
            all_string = str("@id" + user_str)
            for each in all_string:
                users_ids.append(all_string)
                break
            break
        break

count = len(users_ids)
those_ids = ', '.join(users_ids)

message = "Уважаемые Свидетели Скандала! " \
          "С этой недели Святая Инквизиция в лице Админа с помощью разящего меча одолженного у Люка Скайуокера" \
          " с твердой рукой, будет предавать анафеме усомнившихся в силе Скандала. Будем изгонять бесов. Публично. " \
          "Исцеление бесноватого отрока будет проходить путем сжигания на виртуальном костре публичного порицания. " \
          "И оповещения всех Свидетелей о том «Кто» усомнился. А проще - запускаем стену позора " \
          "преданных бану грешников. " \
          "\n" \
          "\n" \
          "Список добрых дел для получения индульгенции:" \
          "\n" \
          "1. Признание грехов" \
          "\n" \
          "2. Покаяние перед Админом." \
          "\n" \
          "3. Получение публичных порок от всех Свидетелей Скандала." \
          "\n" \
          "\n" \
          "Они попали В задний проход Ада:  "

message_text = (message + those_ids)

typical_kirovohrad = "-46631810"
scandal_kirovohrad = "-80849532"
typical_kirovohrad_boss = "13147598"

wall_post = vkapi('wall.post',
                  owner_id=scandal_kirovohrad,
                  from_group='1',
                  message=message_text,
                  attachments='photo-80849532_391644338,'
                              'audio13147598_414979530,',
                  signed='0')

print("Message has been posted successfully!")
print(count)
print(message_text)
