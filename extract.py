# coding：utf-8
import requests
import json
import random

"""
id:帖子ID
floor_threshold：限制楼层 必填
rep_cnt：抽出人数 
word：评论所要包含的词语，多个用逗号分割
"""
def extract(id: int, floor_threshold, rep_cnt, word):
    id = int(0 if id is None else id)
    floor_threshold = int(0 if floor_threshold is None else floor_threshold)
    rep_cnt = int(0 if rep_cnt is None else rep_cnt)
    rep_cnt = int(0 if rep_cnt is None else rep_cnt)
    word = str("" if word is None else word)

    word_list = word.split(",")
    page = int(floor_threshold / 20)
    last_range = floor_threshold % 20
    url_list = []  # 请求页面
    last_id = 0
    for x in range(0, page):
        url_ = 'https://bbs-api.mihoyo.com/post/wapi/getPostReplies?gids=2&is_hot=false&last_id=%d&order_type=1&post_id=%d&size=20' % (
            last_id, id)
        url_list.append(url_)
        last_id += 20

    if last_range > 0:
        url_ = 'https://bbs-api.mihoyo.com/post/wapi/getPostReplies?gids=2&is_hot=false&last_id=%d&order_type=1&post_id=%d&size=%d' % (
            last_id, id, last_range)
        url_list.append(url_)

    candidate_ = []
    candidate_person_list = []  # 候选人列表
    # print("楼层|昵称|评论")
    for url_ in url_list:
        requests_data = requests.get(url_).content.decode("utf-8")
        data = json.loads(requests_data)
        data = data['data']['list']
        for rep in data:
            rep_ = rep['reply']
            content = str(rep_['content']).split("</p>")[0].replace("<p>", "").replace('\n', '')
            floor_id = rep_['floor_id'] + 1
            user = rep['user']
            uid = user['uid']
            nickname = user['nickname']
            if nickname not in candidate_ and floor_id <= floor_threshold:  # 关键词提取并去重
                # print(nickname, floor_id, content)
                candidate_.append(nickname)
                candidate_person_list.append([nickname, floor_id, content])

    return_list = []
    candidate_person_list_last = []  # 候选人最终列表

    if len(word_list) > 0:
        for person in candidate_person_list:
            for word_ in word_list:
                # 判断 评论中包含词语，并且评论人不在最终候选人中
                if word_ in person[2] and person not in candidate_person_list_last:
                    # 满足条件后最终候选人中添加此候选人
                    candidate_person_list_last.append(person)
    return_list = []
    for x in range(1, rep_cnt + 1):
        index = random.randint(0, len(candidate_person_list_last) - 1)
        # print("第 %d 个中奖者：%s" % (x, candidate_person_list[index]))
        key = 'p' + str(x)
        nickname = candidate_person_list_last[index][0]
        floor_id = candidate_person_list_last[index][1]
        content = candidate_person_list_last[index][2]
        content_text = candidate_person_list_last[index][2]
        img = candidate_person_list_last[index][2]
        # 去除评论中的格式
        while '<div ' in content_text:
            index_1 = content_text.index("""<div class="ql-image"><div class="ql-image-box">""")
            index_2 = content_text.index("""<div class="ql-blot-del"></div></div></div>""")
            x1 = content_text[index_1:index_2 + 43]
            content_text = content_text.replace(x1, '')
        # 提取首个图片
        if 'https:' in img and '.jpg' in img:
            index_1 = img.index("""https:""")
            index_2 = img.index(""".jpg""")
            img = img[index_1:index_2 + 4]


        # return_list.append({'pn':x,'nickname': nickname, 'floor_id': floor_id, 'content_text': content_text, 'img': img})
        # 使用字符串作为函数返回值目的为了方便后续处理，如果值作为抽奖不使用其他的话可以使用上一行代码，使用list作为返回值
        return_list.append(str(x) + '|-|' + nickname + '|-|' + str(floor_id) + '|-|' + content_text + '|-|' + img)
        candidate_person_list_last.remove(candidate_person_list_last[index])
    return_list_last = '||-||'.join(return_list)
    return return_list_last


