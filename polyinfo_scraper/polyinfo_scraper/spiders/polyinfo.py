import scrapy
import json
import logging
from scrapy_splash import SplashRequest
# import requests

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    logging.info(response.text)
    # if response.status == 200:
    #     return False
    noscript = response.xpath('//noscript/text()').get()
    if noscript is None:
        return False
    # for info in success:
        
    #     if "failed" in info:
    #         return True
    # return False
    return True

class PolyinfoSpider(scrapy.Spider):
    name = 'polyinfo'
    # allowed_domains = ['https://polymer.nims.go.jp/PoLyInfo/']
    # TODO: how to login?
    
    search_url = "https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p-search.cgi/"
    login_url = "https://mdpf-cas.nims.go.jp/cas/login?service="\
        + "https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p"\
        +"-search.cgi"
    check_js = "https://www.whatismybrowser.com/detect/is-javascript-enabled"

    start_urls = [check_js]

    # def start_requests(self):

    #     login_url = "https://mdpf-cas.nims.go.jp/cas/login?service="\
    #     + "https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p"\
    #     +"-search.cgi"

    #     email = input('Enter PoLyInfo username: ')
    #     password = input('Enter PoLyInfo Password: ')

    #     formdata={'username': email, 'password': password}

    #     yield scrapy.FormRequest(
    #         url=login_url,
    #         formdata=formdata,
    #         callback=self.after_login
    #     )

    def parse(self, response):

        # splash_url = "http://localhost:8050/render.json"
        # body = {'url': login_url,
        #         "har": 1, 
        #         "html": 0
        # }

        # script to handle login page
        # ...
        script = """
            function main(splash)
                splash:init_cookies(splash.args.cookies)

                assert(splash:go{
                    url=splash.args.url,
                    http_method=splash.args.http_method,
                })
                
                assert(splash:wait(0.5))
                --splash:runjs(splash.args.js_source)
                --splash:runjs("document.getElementsByTagName("script")")
                splash:runjs("document.type='text/javascript'")

                --local entries = splash:history()
                --local last_response = entries[#entries].response
                return {
                    url = splash:url(),
                    --headers = last_response.headers,
                    --http_status = last_response.status,
                    cookies = splash:get_cookies(),
                    html = splash:html()
                }
            end
            """
        # ...

        yield SplashRequest(
            self.login_url,
            self.sendCookie,
            endpoint='/execute',
            # endpoint='render.html',
            meta={'cookiejar': "1"},
            args={'url': self.login_url,
                  'wait': 0.5,
                  'http_method': 'GET',
                  'js_source': 'document.type="text/javascript";',
                  'lua_source': script,
                  'cookies': '',  
            },
        )

        # return scrapy.Request(
        #     url="https://www.whatismybrowser.com/detect/is-javascript-enabled",
        #     method='GET',
        #     # body=formdata,
        #     # body=json.dumps(body),
        #     callback=self.login
        # )

    def sendCookie(self, response):

        # script to handle login page
        # ...
        script = """
            function main(splash)
                splash:init_cookies(splash.args.cookies)

                assert(splash:go{
                    url=splash.args.url,
                    http_method=splash.args.http_method,
                })
                
                assert(splash:wait(0.5))
                --splash:runjs(splash.args.js_source)
                --splash:runjs("document.getElementsByTagName("script")")
                splash:runjs("document.type='text/javascript'")

                --local entries = splash:history()
                --local last_response = entries[#entries].response
                return {
                    url = splash:url(),
                    --headers = last_response.headers,
                    --http_status = last_response.status,
                    cookies = splash:get_cookies(),
                    html = splash:html()
                }
            end
            """
        # ...

        yield SplashRequest(
            self.login_url,
            self.login,
            endpoint='/execute',
            # endpoint='render.html',
            meta={'cookiejar': '1'},
            args={'url': self.login_url,
                  'wait': 0.5,
                  'http_method': 'GET',
                  'js_source': 'document.type="text/javascript";',
                  'lua_source': script,
                  'cookies': response.meta['cookiejar'],
            },
        )

    def login(self, response):
        self.logger.info(response)
        if authentication_failed(response):
            self.logger.error("Get login page failed")
            return

        # the execution string from response html
        # exec = response.xpath('//input[@name="execution"]/value()').get()
        exec = response.xpath('//input[@name="execution"]/@value').get()
        email = input('Enter PoLyInfo username: ')
        password = input('Enter PoLyInfo Password: ')
        # continue scraping with authenticated session...

        formdata = {'username': email,
                    'password': password,
                    'execution': exec,
                    '_eventId': 'submit',
                    'geolocation': ''
        }

        return SplashRequest(
            self.login_url,
            self.search_page,
            endpoint='render.html',
            # meta={'cookiejar': response.meta['cookiejar']},
            args={'wait': 0.5,
                  'http_method': 'POST',
                  'cookies': response.meta['cookiejar']['1'],
                #   'lua_source': self.script,
                  'body': json.dumps(formdata)
            }
        )

    def search_page(self, response):
        if response.status == 302:
            logging.info("Success on search page!")
            return
        else:
            logging.info("Failed to get to search page!")
            return

        # TODO: how to submit correct request payload?
        # p-type=Homopolymer%21Copolymer%21Blend
        # p-prop1-name=7110%3B1
        req_body = "p-type=Homopolymer%21Copolymer%21Blend&"\
            + "p-name-string=substring&"\
            + "p-cu-atom1=C&"\
            + "p-cu-atom2=H&"\
            + "p-prop1-name=7110%3B1&"\
            + "p-refer-other-string=substring&"\
            + "search=Search"
        scrapy.http.Request.replace(body = req_body)

        yield SplashRequest(
            self.search_url,
            self.process_data,
            args={'wait': 0.5,
                  'http_method': 'GET',
                  'body': json.dumps(formdata)
            }
        )

    def process_data(self, response):
        # TODO: what if result is a list of different things in 'dark_noneborder'?
        molecule_name = response.xpath('//a[@href="/PoLyInfo/cgi-bin/pi-id-search.cgi?PID=*"]/text()').get()
        melt_viscosity = response.xpath('//td[@class="dark_noneborder"]/text()').get()
        return {"molecule": molecule_name, "melt_viscosity": melt_viscosity}

        # TODO: get results from all pages?
        # TODO: write to csv file?