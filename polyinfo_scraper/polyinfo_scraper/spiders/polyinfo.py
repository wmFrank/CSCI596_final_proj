import scrapy
import json
import logging

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    logging.info(response.text)
    if response.status == 302:
        return False
    # success = response.xpath('//p/text()').getall()
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

    start_urls = [login_url]

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
        email = input('Enter PoLyInfo username: ')
        password = input('Enter PoLyInfo Password: ')

        login_url = "https://mdpf-cas.nims.go.jp/cas/login"

        # login_url = "https://mdpf-cas.nims.go.jp/cas/login?service="\
        #     + "https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p"\
        #     +"-search.cgi"

        formdata = {'username': email, 'password': password}

        yield scrapy.Request(
            url=login_url,
            method='POST',
            # body=formdata,
            body=json.dumps(formdata),
            callback=self.after_login
        )

    def after_login(self, response):
        self.logger.info(response)
        if authentication_failed(response):
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...

        search_url = "https://polymer.nims.go.jp/PoLyInfo/cgi-bin/p"\
        +"-search.cgi"

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

        yield scrapy.Request(
            url=search_url,
            # formdata=formdata,
            callback=self.process_data
        )

    def process_data(self, response):
        # TODO: what if result is a list of different things in 'dark_noneborder'?
        molecule_name = response.xpath('//a[@href="/PoLyInfo/cgi-bin/pi-id-search.cgi?PID=*/text()"]').get()
        melt_viscosity = response.xpath('//td[@class="dark_noneborder"]/text()').get()
        return {"molecule": molecule_name, "melt_viscosity": melt_viscosity}

        # TODO: get results from all pages?
        # TODO: write to csv file?