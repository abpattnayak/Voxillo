# coding=utf-8
from __future__ import absolute_import
import re
import datetime
from voxillo.items import VoxilloItem
from scrapy import log

def ing_scraper(productName, selector, validSinceDate):
    dlist = []
    log.msg("Hello", level = log.DEBUG)
    #tables
    tables =  selector.xpath('//table[@class="table table-b table-lr-unpadded l-mb-0"]/tbody')
    #log.msg("tables  --------- %s" %tables.xpath("text()").extract(), level = log.DEBUG)
    now = datetime.datetime.now()
    
    for i in range(0,2): #tables
        rows = tables[i].xpath("tr")
        headers = tables[i].xpath("tr/td/strong/text()").extract()
        for j in range(1,len(rows)):
            datas = rows[j].xpath("td/text()").extract()
            for k in range(1, len(datas)):
                item = {}
                #Country Code, Provider Name
                item['CountryCode'] = "NL"
                item['ProviderName'] = "ING"
                #Product Name
                item['ProductName'] = "ING"+productName
                #Loan Type
                item['LoanType'] = productName
                #Period
                item['Period'] = removeJaar(datas[0])
                #Interest Rate
                data = formatUnicode(datas[k])
                data = removeSpecial(data.encode("utf-8").strip())
                item['Rate'] = str(float(data)+0.25)
                #Coverage Start
                if(headers[k-1] == ">101%"):
                    item['CoverageStart'] = "101"
                else:
                    item['CoverageStart'] = ""
                #Coverage End
                nonBreakSpace = u'\xa0'
                coverageEnd = headers[k-1].replace(nonBreakSpace,"")
                coverageEnd = removeSpecial(formatUnicode(coverageEnd.encode("utf-8").strip()))
                if(headers[k-1] != ">101%" and coverageEnd != "NHG"):
                    item['CoverageEnd'] = coverageEnd                   
                else:
                    item['CoverageEnd'] = ""
                #Check Date
                item['CheckDate'] = str(now.strftime("%Y-%m-%d"))
                #Valid Since Date
                item['ValidSince'] = validSinceDate
                #NHG
                if(coverageEnd!="NHG"):
                    item['NHG'] = "N"
                else:
                    item['NHG'] = "Y"
                dlist.append(item)
    return dlist

def removeJaar(str):
	str = str.replace("jaar","")
	return str

def removeSpecial(str):
	str = str.replace("%","").replace("≤","").replace(">","")
	return str

def formatUnicode(str):
	str = str.replace(",",".").replace("']","").replace("[u'","")
	return str