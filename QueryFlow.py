#! /usr/bin/env python
#coding=utf-8

from BeautifulSoup import BeautifulSoup
import requests

#ip_info = None 全局变量！ 尽量不要使用全局变量，因为生成的exe会报错

def get_my_ip():
    #从校园网上获取IP信息
    doc = requests.get('http://www.twt.edu.cn/service/')
    soup = BeautifulSoup(doc.content)
    ips = soup('form', action="http://nc.tju.edu.cn/query/ipFlow.asp")[0]('input')
    ip_input = {}
    for input in ips:
        ip_input[input['name']] = input['value']
    return ip_input

def get_ip_string(ip_info):
    ip_string = '%s.%s.%s.%s' %(ip_info['ip1'].decode('ascii'),ip_info['ip2'],ip_info['ip3'],ip_info['ip4'])
    return ip_string

def get_fee(ip):
    #获取费用网页
    payload = {'ip': ip}
    r = requests.post("http://nc.tju.edu.cn/query/feeQuery.asp", data=payload)
    doc = r.content
    soup = BeautifulSoup(doc)
    #找到费用
    fee = soup('font', color="#ff0000")[0].b.string.strip()
    return fee

def get_flow_info(ip_info):
    #查找流量信息
    payload = {'ip1':ip_info['ip1'], 'ip2':ip_info['ip2'],
                'ip3':ip_info['ip3'], 'ip4':ip_info['ip4'],
                'year1':ip_info['year1'], 'month1':ip_info['month1']}
    r = requests.post("http://nc.tju.edu.cn/query/ipFlow.asp", data=payload)
    doc = r.content
    soup = BeautifulSoup(doc)
    #找到时间栏
    date_list_doc = soup('td', height="17", colspan="2", bgcolor="#FFFFFF")
    date_list = [td.div.string.strip() for td in date_list_doc]
    #找到流量栏
    flow_list_doc = soup('td', width="331", height="17", bgcolor="#FFFFFF")
    flow_list = [td.div.string.strip() for td in flow_list_doc]
    #合并时间和流量
    flow_info = zip(date_list, flow_list)
    return flow_info

def print_query_result(ip, ip_info, flow_info, fee):
    #标题
    print u"\n        流量信息查询\n".encode('gbk')
    #本机ip信息
    print "{:<20}{:<20}".format(u"当前查询的IP为：".encode('gbk'), ip)
    print "{:<20}{:<20}\n".format(u"当前查询的日期为：".encode('gbk'),
                                    u"{}年{}月".encode('gbk').format(ip_info['year1'].encode('gbk'),ip_info['month1'].encode('gbk')))
    #当月总信息
    print "{:<20}{:<20}".format(u"当月月流量为：".encode('gbk'),
                                    "%s (MB)".encode('gbk') % flow_info[0][1])
    print "{:<20}{:<20}\n\n".format(u"当前账户余额为：".encode('gbk'),
                                    u"%s (元)".encode('gbk') % fee.encode('gbk'))
    #当月流量详细
    print u"当月日流量详细为：\n".encode('gbk')
    print "  {:15}  {:10}".format(u'    日期'.encode('gbk'), u'    流量'.encode('gbk'))
    for date,flow in flow_info[1:]:
        print "  {:<15}  {:>10}".format(date.encode('gbk'), flow.encode('gbk'))
    print '\n'
    #命令窗口退出
    while True:
        s = raw_input(u"退出请按 'q' 并回车\n>>>".encode('gbk'))
        if s == 'q':
            break
    return

def run():
    #获得本机的IP信息
    ip_info = get_my_ip()
    #获得ip字符串
    ip = get_ip_string(ip_info)
    #获得流量信息
    flow_info = get_flow_info(ip_info)
    #获得费用信息
    fee = get_fee(ip)
    #输出全部信息
    print_query_result(ip, ip_info,flow_info, fee)
    return


if __name__ == '__main__':
    run()



