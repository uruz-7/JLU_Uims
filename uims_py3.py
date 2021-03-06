#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""It works."""

import json
import hashlib
import requests

NAME = ''
PWDPLAIN = ''
ANSWERS = {'prob11': 'A', 'prob12': 'A', 'prob13': 'A', 'prob14': 'A', 'prob15': 'A',
           'prob21': 'A', 'prob22': 'A', 'prob23': 'A',
           'prob31': 'A', 'prob32': 'A',
           'prob41': 'A', 'prob42': 'A', 'prob43': 'A',
           'prob51': 'A', 'prob52': 'A',
           'sat6': 'A',
           'mulsel71': 'EGHK',
           'advice8': 'good'}

def maketransferpwd(name, pwdplain):
    """Transfer the passwd."""
    inp = hashlib.md5('UIMS'.encode('utf-8')
                      + name.encode('utf-8')
                      + pwdplain.encode('utf-8')).hexdigest()
    return inp

def login(name, inp):
    """It's for login and evaluation."""
    itemid = []
    s_session = requests.session()
    param = {'j_username': name, 'j_password': inp}
    s_session.post('http://uims.jlu.edu.cn/ntms/j_spring_security_check', param)
    userinfo = s_session.post(('http://uims.jlu.edu.cn/ntms'
                               '/action/getCurrentUserInfo.do'))
    userid = json.loads(userinfo.text)['userId']
    search = json.dumps({"type": "search", "tag": "blankEvalItem",
                         "branch": "default", "params": {"personId": userid}})
    headers_foo = {'Content-Type': 'application/json;charset=UTF-8'}
    result = s_session.post('http://uims.jlu.edu.cn/ntms/service/res.do',
                            search, headers=headers_foo)
    dic_foo = json.loads(result.text)

    for i in dic_foo['value']:
        itemid.append(i['evalItemId'])

    headers = {'Content-Type': 'application/json'}

    for item in itemid:
        dic = {'evalItemId': item, "answers": ANSWERS}
        data = json.dumps(dic)
        fuck_p = s_session.post(('http://uims.jlu.edu.cn/ntms'
                                 '/eduEvaluate/eval-with-answer.do'),
                                data, headers=headers)
        data_dict = json.loads(data)
        print(data_dict['evalItemId'], fuck_p.text)

if __name__ == '__main__':
    login(NAME, maketransferpwd(NAME, PWDPLAIN))
