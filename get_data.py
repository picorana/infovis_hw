import wptools
import json
from pprint import pprint

franchises = ["Crash Bandicoot"]
wiki_langs = ['en', 'de', 'fr', 'es', 'ru', 'ja', 'nl', 'it', 'sv', 'pl', 'vi', 'pt', 'ar', 'zh', 'uk', 'ca', 'no', 'fi', 'cs', 'hu', 'ro', 'ko', 'da', 'sr', 'id', 'he', 'fa', 'th', 'ei', 'hi', 'tr']
wiki_langs_dict = {
	'en':'English', 'de':'German', 'fr':'French', 'es':'Spanish', 'ru':'Russian', 'it': 'Italian', 'sv':'Swedish', 
	'ja':'Japanese', 'nl':'Dutch', 'pl':'Polish', 'vi':'Vietnamese', 'pt':'Portuguese', 'ar':'Arabic', 'zh':'Chinese', 
	'uk':'Ukrainian', 'ko':'Korean', 'ca':'Catalan', 'no':'Norwegian', 'fi':'Finnish', 'cs':'Czech', 'hu':'Hungarian', 'ro':'Romanian', 'da':'Danish'
}
outdict = {'langs':[]}
errorlog = open('errorlog.txt', 'w')


"""
for franchise in franchises:
	page = wptools.page(franchise)
	#page.get_parse()
	#for elem in page.data['infobox']:
	#	print(elem)
	page.get_wikidata()
	print(page.data['wikidata'])
"""

for lang in wiki_langs_dict:
	try:
		site = wptools.site()
		site.top(lang + '.wikipedia.org')

		lang_dict = {'shortname': lang, 'longname': wiki_langs_dict[lang], 'top_articles':[]}

		for i in range(0, 25):
			p = site.data['mostviewed'][i]
			try:
				page = wptools.page(p['title'])
				page.get_more()
				if 'categories' in page.data:
					p['categories'] = page.data['categories']
			except:
				print('exception fetching categories on ' + p['title'])
				errorlog.write('exception fetching categories on ' + p['title'])

			try:
				page = wptools.page(p['title'])
				page.get_wikidata()
				if 'what' in page.data:
					p['what'] = page.data['what']
			except:
				print('exception fetching what on ' + p['title'])
				errorlog.write('exception fetching what on ' + p['title'])

			lang_dict['top_articles'].append(p)

		outdict['langs'].append(lang_dict)
		json.dump(outdict, open('top_wiki.json', 'w'), indent=4)
	except:
		print('exception on lang '+ lang)
		errorlog.write('exception on lang '+ lang)
	





	