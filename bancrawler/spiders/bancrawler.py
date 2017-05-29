import scrapy
import re

class colgcrawler(scrapy.Spider):
    name = 'bancrawler'
    start_urls = [
        'http://bbs.colg.cn/thread-4747709-1-1.html',
        'http://bbs.colg.cn/thread-4542707-1-1.html',
        'http://bbs.colg.cn/thread-4496807-1-1.html',
        'http://bbs.colg.cn/thread-4387439-1-1.html',
        'http://bbs.colg.cn/thread-4271185-1-1.html',
        'http://bbs.colg.cn/thread-4200263-1-1.html',
        'http://bbs.colg.cn/thread-4113372-1-1.html',
        'http://bbs.colg.cn/thread-4054050-1-1.html',
        'http://bbs.colg.cn/thread-4028257-1-1.html'        
        ]

    def parse(self, response:scrapy.http.Response):
        postmatch = re.compile(r'\s*ID[:：\s]+(.+)\s+帖.*\s+楼.*\s+天[^:：]*[:：\s]+(.+)\s+原[^:：]*[:：\s]+(.*)')               ##用于辨析禁言格式的regex语句. .group(1)=ID, .group(2)=天数, group(3)=原因
        posts = response.xpath('//div[@class="dfsj_post mbm"]')                                                                 ##找出所有楼层
        for post in posts:
            bannerusername = post.xpath('descendant::a[@class="xw1"]/text()').extract_first()                                   ##禁言人
            posttext = ''.join(post.xpath('descendant::td[@class="t_f"]/descendant-or-self::text()').extract())                 ##文章内容
            postmatched = postmatch.match(posttext)                                                                             ##regex match                
            if postmatched:
                userid = postmatched.group(1).strip('\r')
                duration = postmatched.group(2).strip('\r')
                reason = postmatched.group(3).strip('\r')
                extraction = {
                    'bannerusername': bannerusername,
                    'userid': userid,
                    'duration': duration,
                    'reason': reason
                    }
                yield extraction

        next_page = response.xpath('//a[@class="bm_h"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)