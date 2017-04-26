#-*- coding: utf-8 -*-
import requests


social_type = "facebook"
def get_userinfo_from_facebook(token):

    URL = 'https://graph.facebook.com/me'
    require_fields = [
        'id',
        'name',
        'birthday',
        'email',
        'age_range',
        'about',
        'devices',
        'first_name',
        'gender',
        'last_name',
        'locale',
        'middle_name',
        'timezone',
    ]
    fields = ""
    for field in require_fields:
        fields = fields + field +', '
    # print(fields)
    fields = fields[:-2]
    # print(fields) # 뒤에 , 제거

    params = {'access_token': token,
              'fields': fields}

    try:
        r = requests.get(URL, params=params)
        r = r.json()
    except:
        print(r['error'])
        return r

    # utf-8 = unicode(euckr, 'euc-kr').encode('utf-8')
    if 'id' in r:
        print("id is not None")
        pic_request_url = "https://graph.facebook.com/" + r['id']+"/picture"
        pic_url = requests.get(pic_request_url , params= {'access_token': token}).url
    else:
        print("id is None, invalid facebook token")
        # error
        return r

    # 자동생성아디 facebook_id
    r['username'] = social_type+"_"+r['id']
    print('generated username : '+r['username'])
    del r['id']

    return {**r, **{'pic_url': pic_url}}