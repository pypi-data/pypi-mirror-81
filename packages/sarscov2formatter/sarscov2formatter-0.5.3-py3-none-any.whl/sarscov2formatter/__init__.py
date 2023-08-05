#!/usr/bin/env python
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import pandas as pd
import requests
import sys
import json
import yaml
import datetime

# Checks that date is in correct format
def validate_date(date_text):
	try:
		datetime.datetime.strptime(date_text, '%Y%m%d')
		return 0
	except:
		return 1

# Dictionary of regions for each country
regions = {'Andorra': 'Europe', 'Afghanistan': 'Asia', 'Antigua and Barbuda': 'North America', 'Albania': 'Europe', 'Armenia': 'Asia', 'Angola': 'Africa', 'Argentina': 'South America', 'Austria': 'Europe', 'Australia': 'Oceania', 'Azerbaijan': 'Asia', 'Barbados': 'North America', 'Bangladesh': 'Asia', 'Belgium': 'Europe', 'Burkina Faso': 'Africa', 'Bulgaria': 'Europe', 'Bahrain': 'Asia', 'Burundi': 'Africa', 'Benin': 'Africa', 'Brunei Darussalam': 'Asia', 'Bolivia': 'South America', 'Brazil': 'South America', 'Bahamas': 'North America', 'Bhutan': 'Asia', 'Botswana': 'Africa', 'Belarus': 'Europe', 'Belize': 'Central America', 'Canada': 'North America', 'Democratic Republic of the Congo': 'Africa', 'Republic of the Congo': 'Africa', "CÃ´te d'Ivoire": 'Africa', 'Chile': 'South America', 'Cameroon': 'Africa', "Peoples Republic of China": 'Asia', "China": 'Asia', 'Colombia': 'South America', 'Costa Rica': 'Central America', 'Cuba': 'North America', 'Cape Verde': 'Africa', 'Cyprus': 'Asia', 'Czech Republic': 'Europe', 'Germany': 'Europe', 'Djibouti': 'Africa', 'Denmark': 'Europe', 'Dominica': 'North America', 'Dominican Republic': 'North America', 'Ecuador': 'South America', 'Estonia': 'Europe', 'Egypt': 'Africa', 'Eritrea': 'Africa', 'Ethiopia': 'Africa', 'Finland': 'Europe', 'Fiji': 'Oceania', 'France': 'Europe', 'Gabon': 'Africa', 'Georgia': 'Asia', 'Ghana': 'Africa', 'The Gambia': 'Africa', 'Guinea': 'Africa', 'Greece': 'Europe', 'Guatemala': 'Central America', 'Haiti': 'North America', 'Guinea-Bissau': 'Africa', 'Guyana': 'South America', 'Honduras': 'Central America', 'Hungary': 'Europe', 'Indonesia': 'Asia', 'Republic of Ireland': 'Europe', 'Israel': 'Asia', 'India': 'Asia', 'Iraq': 'Asia', 'Iran': 'Asia', 'Iceland': 'Europe', 'Italy': 'Europe', 'Jamaica': 'North America', 'Jordan': 'Asia', 'Japan': 'Asia', 'Kenya': 'Africa', 'Kyrgyzstan': 'Asia', 'Kiribati': 'Oceania', 'North Korea': 'Asia', 'South Korea': 'Asia', 'Kuwait': 'Asia', 'Lebanon': 'Asia', 'Liechtenstein': 'Europe', 'Liberia': 'Africa', 'Lesotho': 'Africa', 'Lithuania': 'Europe', 'Luxembourg': 'Europe', 'Latvia': 'Europe', 'Libya': 'Africa', 'Madagascar': 'Africa', 'Marshall Islands': 'Oceania', 'Macedonia': 'Europe', 'Mali': 'Africa', 'Myanmar': 'Asia', 'Mongolia': 'Asia', 'Mauritania': 'Africa', 'Malta': 'Europe', 'Mauritius': 'Africa', 'Maldives': 'Asia', 'Malawi': 'Africa', 'Mexico': 'North America', 'Malaysia': 'Asia', 'Mozambique': 'Africa', 'Namibia': 'Africa', 'Niger': 'Africa', 'Nigeria': 'Africa', 'Nicaragua': 'Central America', 'Kingdom of the Netherlands': 'Europe', 'Norway': 'Europe', 'Nepal': 'Asia', 'Nauru': 'Oceania', 'New Zealand': 'Oceania', 'Oman': 'Asia', 'Panama': 'Central America', 'Peru': 'South America', 'Papua New Guinea': 'Oceania', 'Philippines': 'Asia', 'Pakistan': 'Asia', 'Poland': 'Europe', 'Portugal': 'Europe', 'Palau': 'Oceania', 'Paraguay': 'South America', 'Qatar': 'Asia', 'Romania': 'Europe', 'Russia': 'Europe', 'Rwanda': 'Africa', 'Saudi Arabia': 'Asia', 'Solomon Islands': 'Oceania', 'Seychelles': 'Africa', 'Sudan': 'Africa', 'Sweden': 'Europe', 'Singapore': 'Asia', 'Slovenia': 'Europe', 'Slovakia': 'Europe', 'Sierra Leone': 'Africa', 'San Marino': 'Europe', 'Senegal': 'Africa', 'Somalia': 'Africa', 'Suriname': 'South America', 'Syria': 'Asia', 'Taiwan': 'Asia', 'Togo': 'Africa', 'Thailand': 'Asia', 'Tajikistan': 'Asia', 'Turkmenistan': 'Asia', 'Tunisia': 'Africa', 'Tonga': 'Oceania', 'Turkey': 'Asia', 'Trinidad and Tobago': 'North America', 'Tuvalu': 'Oceania', 'Tanzania': 'Africa', 'Ukraine': 'Europe', 'Uganda': 'Africa', 'USA': 'North America', 'United States': 'North America', 'Uruguay': 'South America', 'Uzbekistan': 'Asia', 'Vatican City': 'Europe', 'Venezuela': 'South America', 'Vietnam': 'Asia', 'Vanuatu': 'Oceania', 'Yemen': 'Asia', 'Zambia': 'Africa', 'Zimbabwe': 'Africa', 'Algeria': 'Africa', 'Bosnia and Herzegovina': 'Europe', 'Cambodia': 'Asia', 'Central African Republic': 'Africa', 'Chad': 'Africa', 'Comoros': 'Africa', 'Croatia': 'Europe', 'East Timor': 'Asia', 'El Salvador': 'Central America', 'Equatorial Guinea': 'Africa', 'Grenada': 'North America', 'Kazakhstan': 'Asia', 'Laos': 'Asia', 'Federated States of Micronesia': 'Oceania', 'Moldova': 'Europe', 'Monaco': 'Europe', 'Montenegro': 'Europe', 'Morocco': 'Africa', 'Saint Kitts and Nevis': 'North America', 'Saint Lucia': 'North America', 'Saint Vincent and the Grenadines': 'North America', 'Samoa': 'Oceania', 'Serbia': 'Europe', 'South Africa': 'Africa', 'Spain': 'Europe', 'Sri Lanka': 'Asia', 'Swaziland': 'Africa', 'Switzerland': 'Europe', 'United Arab Emirates': 'Asia', 'United Kingdom': 'Europe'}

# US states abbreviations dictionary
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def fixVietnam(instring):
	if instring == 'Viet Nam':
		return 'Vietnam'
	else:
		return instring


def formatter(align, meta_source):
# Create dictionary of duplicate sequences and list of all accession IDs
	multi_seqs = {}
	all_acc = []
	records = []
	for record in SeqIO.parse(align, 'fasta'):
		if record.description[:8] == 'MultiSeq':
			nodots = [x[:-2] for x in record.description.split(' ')[1].split(',') if x[-2] == '.']
			multi_seqs[record.description.split(' ')[0]] = nodots
			all_acc.extend(nodots)
		else:
			all_acc.append(record.id)
		if record.id[-2] == '.':
			records.append(SeqRecord(record.seq, id=record.id[:-2], description=''))
		else:
			records.append(SeqRecord(record.seq, id=record.id, description=''))
	all_acc = [a[:-2] if a[-2] == '.' else a for a in all_acc]


	# Create metadata file
	# If ncbi, get metadata from ncbi, otherwise from file
	meta = {}
	invalid = []
	if meta_source == 'ncbi':
		url = 'https://www.ncbi.nlm.nih.gov/projects/genome/sars-cov-2-seqs/ncov-sequences.yaml'
		request = requests.get(url, allow_redirects=True)
		data = yaml.load(request.content, Loader=yaml.FullLoader)
		for item in data['genbank-sequences']:
			check = 0
			if item['accession'] in all_acc:
				acc = item['accession']
				date = item['collection-date'].replace('-', '')
				if len(date) == 6:
					if acc == 'NC_045512':
						date = '20200117'
					else:
						invalid.append(acc)
						check = 1
				if check == 0:
					location = item['country']
					try:
						if ':' in location and ',' in location:
							country = fixVietnam(location.split(':')[0])
							subregion = regions[country]
							if country == 'China':
								state = location.split(' ')[1][:-1]
								locality = location.split(',')[1][1:]
							elif country == 'USA':
								comma = location.index(',')
								location = location[:comma+1]+location[comma+2:]
								state_local = location.split(':')[1][1:]
								if len(state_local.split(',')[1]) == 2:
									state = states[state_local.split(',')[1]]
									locality = state_local.split(',')[0]
								else:
									state = states[state_local.split(',')[0]]
									locality = state_local.split(',')[1]
						elif ':' in location and ',' not in location:
							country = fixVietnam(location.split(':')[0])
							subregion = regions[country]
							state = location.split(':')[1][1:]
							locality = None
						else:
							country = fixVietnam(location)
							subregion = regions[country]
							state = None
							locality = None
						meta[acc] = {
						  'collected': date,
						  'location': {
						    'subregion': subregion,
						    'country': country, 
						    'state': state, 
						    'locality': locality
						  }
						}
					except:
						pass
	else:
		data = pd.read_csv(meta_source, sep='\t')
		data = data.where(pd.notnull(data), None)
		for i in range(len(data)):
			if data.iloc[i]['ID'] in all_acc:
				date = data.iloc[i]['collection_date']
				valid = validate_date(str(date))
				if valid == 0:
					meta[data.iloc[i]['ID']] = {
					  'collected': date,
					  'location': {
					    'subregion': regions[data.iloc[i]['country']],
					    'country': data.iloc[i]['country'],
					    'state': data.iloc[i]['state'],
					    'locality': data.iloc[i]['locality']
					  }
					}
				else:
					invalid.append(data.iloc[i]['ID'])


	# Write metadata to a json file
	with open('meta.json', 'w') as file:
		json.dump(meta, file, indent=1, sort_keys=True)


	# Recreate multi_seqs using only the accession that metadata could be extracted from
	meta_acc = [x for x in meta.keys()]
	meta_multi = {}
	for key in multi_seqs.keys():
		multi_seqs[key] = [x for x in multi_seqs[key] if x in meta_acc]
		if len(multi_seqs[key]) != 0:
			meta_multi[key] = multi_seqs[key]

	# Create duplicates file
	dups = {}
	multi = []
	for key in meta_multi.keys():
		num = ''
		for l in key:
			if l == '_':
				break
			elif l in [str(i) for i in range(10)]:
				num += l
		dupID = key
		dups[dupID] = {}
		count = 1
		multi.append(meta_multi[key][0])
		for acc in meta_multi[key][1:]:
			multi.append(acc)
			dups[dupID][str(count)] = acc
			count += 1
	for m in meta_acc:
		if m not in multi and m[:2] != 'NC':
			dupID = m
			dups[dupID] = {'0': dupID}
	with open('duplicates.json', 'w') as file:
		json.dump(dups, file, indent=1, sort_keys=True)

	# Create aligned fasta file in hyphy compatible format using only accessions that metadata could be extracted from
	meta_records = []
	for record in records:
		if (record.id in meta_acc or record.id in meta_multi.keys()) and record.id[:2] != 'NC':
			meta_records.append(record)
	SeqIO.write(meta_records, 'msa.fasta', 'fasta')

def createID(meta, acc):
	if meta[acc]['location']['state'] != None and len(meta[acc]['location']['state']) == 2:
		loc = states[meta[acc]['location']['state']]
	elif meta[acc]['location']['state'] != None and len(meta[acc]['location']['state']) > 2:
		loc = meta[acc]['location']['state']
	elif meta[acc]['location']['state'] == None:
		loc = meta[acc]['location']['country']
	return acc+'_'+loc+'_'+meta[acc]['collected']+'_null'
