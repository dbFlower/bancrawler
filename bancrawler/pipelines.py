# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import json
import operator
from bancrawler.items import *

class entrypipeline:
    daysmatch = re.compile(r'\b[^0-9+*扣]*([0-9]+(?:[\+\*][0-9]+)*)[^0-9+分]*\b')                                                                     ##用于辨析天数后面的格式.
    def open_spider(self, spider):
        self.bannedmembers = dict()
        self.exiledmembers = dict()
        self.bannermembers = dict()
        self.banreason = dict()
        self.banduration = dict()
    def close_spider(self, spider):
        bannedlist = []
        exiledlist = []
        bannerlist = []
        banreasonlist = []
        bandurationlist = []
        for i in self.bannedmembers.values():
            bannedlist.append(dict(i))
        bannedlist = sorted(bannedlist, key = lambda x: x['accumbans'], reverse = True)
        for i in self.exiledmembers.values():
            exiledlist.append(dict(i))
        exiledlist = sorted(exiledlist, key = lambda x: x['numoftoons'], reverse = True)
        for i in self.bannermembers.values():
            bannerlist.append(dict(i))
        bannerlist = sorted(bannerlist, key = lambda x: x['accumbans'], reverse = True)
        for i in self.banreason.items():
            banreasonlist.append(i)
        banreasonlist = sorted(banreasonlist, key = lambda x: x[1], reverse = True)
        for i in self.banduration.items():
            bandurationlist.append(i)
        bandurationlist = sorted(bandurationlist, key = lambda x: x[1], reverse = True)

        with open('result.txt', 'wb') as f:
            f.write('COLG墓园名人堂\n'.encode('utf-8'))
            f.write('\n被禁言堂\n以下用户用时间以及生命完美诠释了作死的真谛\n'.encode('utf-8'))
            for i in bannedlist:
                f.write('{}: 共被禁言{}次, 总时长{}天. {}被西去.\n'.format(i['username'], i['accumbans'], i['duration'], {False:'未', True:'已'}[i['indefinitely']]).encode('utf-8'))
            f.write('\n驱逐光荣榜\n出于对colg的热爱, 以下人被驱逐后仍不断跑回来, 真是可敬\n'.encode('utf-8'))
            for i in exiledlist:
                f.write('{}: 小号共被逮到{}次.\n'.format(i['exiledname'], i['numoftoons']).encode('utf-8'))
            f.write('\n禁言堂\n以下版主日以继夜夜以继日地禁言, 都是惹不起的可pa存在\n'.encode('utf-8'))
            for i in bannerlist:
                f.write('{}: 共进行{}次操作, 总禁言时长{}天, 西去{}人\n'.format(i['username'], i['accumbans'], i['accumdays'], i['accuminds']).encode('utf-8'))
            f.write('\n最受欢迎的禁言原因有:\n'.encode('utf-8'))
            for i in banreasonlist:
                f.write('{}, 被使用{}次\n'.format(*i).encode('utf-8'))
            f.write('\n最受欢迎的禁言时长有:\n'.encode('utf-8'))
            for i in bandurationlist:
                f.write('{}, 被使用{}次\n'.format(*i).encode('utf-8'))
            f.write('\n本次统计采取2015/05/09至2017/05/27墓园数据. 识别并不是很完美, 也其实并不认识多少被驱逐的人. 如有补充请补充咯\n'.encode('utf-8'))
            f.write('源码: https://github.com/mumingpo/bancrawler'.encode('utf-8'))
        with open('banned.json', 'w') as f:
            json.dump(bannedlist, f)
        with open('exiled.json', 'w') as f:
            json.dump(exiledlist, f)
        with open('banner.json', 'w') as f:
            json.dump(bannerlist, f)
        with open('banreason.json', 'w') as f:
            json.dump(banreasonlist, f)
        with open('banduration.json', 'w') as f:
            json.dump(bandurationlist, f)

    def process_item(self, item, spider):
        bannerusername = item['bannerusername']
        userid = item['userid']
        duration = item['duration']
        reason = item['reason']
        if '尊' in reason or '完' in reason:
            if '尊' in reason: reason = '尊八'
            elif '完' in reason: reason = '完爆哥'
            if reason in self.exiledmembers:                                                                                         ##如果被驱逐的人记录中有名
                self.exiledmembers[reason]['numoftoons'] += 1                                                                        ##小号+1
            else:                                                                                                               ##没有
                newexiledmember = exiled()                                                                                      ##建立新档案
                newexiledmember['exiledname'] = reason
                newexiledmember['numoftoons'] = 1
                self.exiledmembers[reason] = newexiledmember
            if bannerusername in self.bannermembers:
                self.bannermembers[bannerusername]['accuminds'] += 1
                self.bannermembers[bannerusername]['accumbans'] += 1
            else:
                newbannermember = banner()
                newbannermember['username'] = bannerusername
                newbannermember['accumdays'] = 0
                newbannermember['accuminds'] = 1
                newbannermember['accumbans'] = 1
                self.bannermembers[bannerusername] = newbannermember
        elif '西' in duration or '∞' in duration or '无限' in duration or '永久' in duration or '驱逐' in duration:
            if userid in self.bannedmembers:
                self.bannedmembers[userid]['accumbans'] += 1
                self.bannedmembers[userid]['indefinitely'] = True
            else:
                newbannedmember = banned()
                newbannedmember['username'] = userid
                newbannedmember['duration'] = 0
                newbannedmember['accumbans'] = 1
                newbannedmember['indefinitely'] = True
                self.bannedmembers[userid] = newbannedmember
            if bannerusername in self.bannermembers:
                self.bannermembers[bannerusername]['accuminds'] += 1
                self.bannermembers[bannerusername]['accumbans'] += 1
            else:
                newbannermember = banner()
                newbannermember['username'] = bannerusername
                newbannermember['accumdays'] = 0
                newbannermember['accuminds'] = 1
                newbannermember['accumbans'] = 1
                self.bannermembers[bannerusername] = newbannermember
        else:
            days = 0
            daysmatched = self.daysmatch.search(duration)
            if daysmatched:
                days = eval(daysmatched.group(1))
            if userid in self.bannedmembers:
                self.bannedmembers[userid]['duration'] += days
                self.bannedmembers[userid]['accumbans'] += 1
            else:
                newbannedmember = banned()
                newbannedmember['username'] = userid
                newbannedmember['duration'] = days
                newbannedmember['accumbans'] = 1
                newbannedmember['indefinitely'] = False
                self.bannedmembers[userid] = newbannedmember
            if bannerusername in self.bannermembers:
                self.bannermembers[bannerusername]['accumdays'] += days
                self.bannermembers[bannerusername]['accumbans'] += 1
            else:
                newbannermember = banner()
                newbannermember['username'] = bannerusername
                newbannermember['accumdays'] = days
                newbannermember['accuminds'] = 0
                newbannermember['accumbans'] = 1
                self.bannermembers[bannerusername] = newbannermember
        if duration in self.banduration:
            self.banduration[duration] += 1
        else:
            self.banduration[duration] = 1
        if reason in self.banreason:
            self.banreason[reason] += 1
        else:
            self.banreason[reason] = 1
        return item
