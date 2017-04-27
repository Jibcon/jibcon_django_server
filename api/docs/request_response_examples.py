post_SocialSignUpOrIn_request = """
{
    "type": "facebook",
    "token": "EAABisr2Aeb8BAEsC022aIMoZB3ZAHUkQvZCLq30RM5oghnZByj7rGQg2qVdOv1OrZCG6zCYq81LQo7kIfEzMt9ZCHyPgZC39rmSYbVQYOe0jXR4fdMbiAz0WGNSbB2tt2ZBtFuov15FscFhz1h8vUtqWwC49iPvWhQmu3h2RZCZCCsv9arwvPsFrmsZA6qdReXX3N2Ed7KP8WWIX7ZCjavtvAZArBxgrGyP3Eb6IZD",
}
"""

post_SocialSignUpOrIn_response = """
{
    "username": "facebook_747049748802271",
    "email": "pjo901018@naver.com",
    "userinfo":
    {
        "id": 29,
        "full_name": "박재영",
        "age_range": "{\"min\": 21}",
        "gender": "male",
        "pic_url": "https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/14202642_625021034338477_6992400572239206628_n.jpg?oh=bd2188618ba461bdb2a691b3d2016519&oe=598597CF",
        "locale": "ko_KR",
        "user": 38
    },
    "first_name": "재영",
    "last_name": "박",
    "groups":[],
    "user_permissions":[],
    "is_superuser": false,
    "last_login": null,
    "date_joined": "2017-04-27T13:30:44.801533Z"
}
"""

get_user_info_request = """ 
HEADERS
{
    "Authorization": "Token 8e9d4d2c83305fbf98e6f3da195270b9877e6dde"
    "Content-Type": "application/json"
}
"""

get_devices_response = """
[
    {
        "id": 13,
        "deviceCom": "찬주 일렉트로닉스",
        "deviceName": "에어컨",
        "deviceWifiAddr": "127.0.0.1",
        "deviceType": "0",
        "deviceOnOffState": false,
        "user": 38
    },
    {
        "id": 14,
        "deviceCom": "찬주 일렉트로닉스",
        "deviceName": "에어컨",
        "deviceWifiAddr": "127.0.0.1",
        "deviceType": "0",
        "deviceOnOffState": false,
        "user": 38
    },
    {
        "id": 15,
        "deviceCom": "찬주 일렉트로닉스",
        "deviceName": "에어컨",
        "deviceWifiAddr": "127.0.0.1",
        "deviceType": "0",
        "deviceOnOffState": false,
        "user": 38
    }
]
"""
post_devices_request = """
HEADERS
{
    "Authorization": "Token 8e9d4d2c83305fbf98e6f3da195270b9877e6dde"
    "Content-Type": "application/json"
}
BODY
{
    "deviceType": "0"
    "deviceOnOffState": false
    "deviceName": "에어컨"
    "deviceWifiAddr": "127.0.0.1"
}
"""

post_devices_response = """
{
    "id": 25,
    "deviceCom": "찬주 일렉트로닉스",
    "deviceName": "에어컨",
    "deviceWifiAddr": "127.0.0.1",
    "deviceType": "0",
    "deviceOnOffState": false,
    "user": 38
}
"""

get_user_signed_check_request = """
HEADERS
{
    "Authorization": "Token 8e9d4d2c83305fbf98e6f3da195270b9877e6dde"
}
"""

get_user_signed_check_response = """

401 Unauthorized

BODY
{
    "detail": "토큰이 유효하지 않습니다."
}
"""