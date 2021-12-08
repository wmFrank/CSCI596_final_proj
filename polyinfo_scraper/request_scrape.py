import requests
from requests_html import HTMLSession

# session = HTMLSession()
session = requests.Session()

# script to handle login page
# ...
script = """
    function main(splash)

        assert(splash:go(splash.args.url))
        assert(splash:wait(0.5))
        --splash:runjs("document.type='text/javascript'")
        --splash:runjs("document.scripts")

        return {
            html = splash:html()
        }
    end
    """
# ...

# email = input('Enter PoLyInfo username: ')
# password = input('Enter PoLyInfo Password: ')

# formdata = {'username': email,
#             'password': password,
#             'execution': exec,
#             '_eventId': 'submit',
#             'geolocation': ''
# }

# resp = session.get('https://mdpf-cas.nims.go.jp/cas/login?service=https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p-search.cgi')
# session.get('http://localhost:8050/render.html',
#             params={'url': 'https://mdpf-cas.nims.go.jp/cas/login?service=https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p-search.cgi',
#                     'wait': 2,
#             })
response = session.get('http://localhost:8050/render.html',
            params={'url': 'https://mdpf-cas.nims.go.jp/cas/login?service=https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p-search.cgi',
                    'wait': 0.5,
                    'http_method': 'POST',
                    # 'lua_source': script,
            })
# response.html.render()
print(response.request.headers)
print(response.headers)
# print(response.content) # unformatted, has '\n'
print(response.text)