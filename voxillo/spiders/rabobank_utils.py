import scrapy
from scrapy import log
import os
import datetime
from format import doFormattingUnicode, doFormattingProductName, findCoverage

def rabo_scraper(divRow, validSince):
	dlist = []
	now = datetime.datetime.now()
	tableRows = divRow.xpath("div/table/tbody/tr")
	headers = tableRows[0].xpath("td")

	for i in range(1,len(tableRows)):
		tableDatas = tableRows[i].xpath("td")
		for j in range(1,len(tableDatas)):
			#log.msg("XX %s" % str(tableDatas[j].xpath("text()").extract()).replace("[u'","").replace("']",""), level = log.DEBUG)
			item = {}
			productName = doFormattingUnicode(doFormattingProductName((str(divRow.xpath("h2/text()").extract()))))
			#static values
			#Country Code, Provider Name
			item['CountryCode'] = "NL"
			item['ProviderName'] = "Rabobank"
            #Product Name
			item['ProductName'] = "Rabobank"+productName
            #Loan Type
			item['LoanType'] = "Annuiteitenhypotheek"
			#Period
			item['Period'] = doFormattingUnicode(str(tableDatas[0].xpath("text()").extract()))
			#Interest Rate
			item['Rate'] = doFormattingUnicode(str(tableDatas[j].xpath("text()").extract()))
			coverage = doFormattingUnicode(str(headers[j].xpath("strong/text()").extract()))
			coverage = findCoverage(coverage).split()
			coverageStart = coverage[0]
			coverageEnd = coverage[1]
			item['CoverageStart'] = coverageStart
			item['CoverageEnd'] = coverageEnd				
			item['CheckDate'] = str(now.strftime("%Y-%m-%d"))
			item['ValidSince'] = validSince
			item['NHG'] = "N"
			dlist.append(item)
	return dlist