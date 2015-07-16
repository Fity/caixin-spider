# -*- coding: utf-8 -*-


class Spider(object):

    def __init__(self, web_session):
        self.web_session = web_session
        print('init Spider...')

    def run(self):
        print('running now')
