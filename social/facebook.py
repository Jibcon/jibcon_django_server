import requests


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
    print(fields)
    fields = fields[:-2]
    print(fields)

    params = {'access_token': token,
              'fields': fields}



    try:
        r = requests.get(URL, params=params)
        r = r.json()
    except:
        pass

    pic_request_url = "https://graph.facebook.com/" + r['id']+"/picture"
    pic_url = requests.get(pic_request_url , params= {'access_token': token}).url

    return {**r, **{'pic_url': pic_url}}