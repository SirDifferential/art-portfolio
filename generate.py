import json
import os

f = open("./config.json")
confstr = f.read()
f.close()

conf = json.loads(confstr)
artdir = conf['artfolder']
print("generating art for folder: ", artdir)

exts = ['png', 'jpg', 'jpeg']
list1 = os.listdir(artdir)
list2 = []

for f in list1:
	for ext in exts:
		if f.endswith(ext):
			list2.append(f)


def parseFile(f):
	parts = f.split("_")
	if not len(parts) == 4:
		return None
	try:
		data = dict()
		data["id"] = int(parts[0][3:])
		data["dom"] = int(parts[1])
		data["mon"] = int(parts[2])
		data["year"] = int((parts[3].split("."))[0])
		data["filename"] = f

		nfo = artdir + "/" + f.split(".")[0] + ".json"
		try:
			if os.path.isfile(nfo):
				f = open(nfo)
				jsstr = f.read()
				f.close()
				data["info"] = json.loads(jsstr)
		except Exception as e:
			print("failed reading info file: ", nfo, ":", e)
	except Exception as e:
		print("Failed parsing data for: ", f, ":", e)
		return None
	return data

def formEntry(d):
	# Form html for gallery page
	html1 = '<div class="col-sm-6 col-md-4 col-lg-3 item"><a href="https://art.plantmonster.net/pieces/'
	html1 += str(d["id"]) + '.html"'
	html1 += 'data-lightbox="photos"><img class="img-fluid" src="'
	html1 += 'https://plantmonster.net/art/' + d["filename"] + '"></a></div>\n'
	d["html1"] = html1

	# Form html for artwork's own page
	html2 = '<p>Art #' + str(d["id"]) + ' - ' + str(d['dom']) + '.' + str(d['mon']) + '.' + str(d['year']) + '</p>\n'

	if 'info' in d:
		# select fields
		html2 += '<p>' + d['info']['description'] + '</p>\n'
		html2 += '</p>\n'

	d["html2"] = html2

# Writes the main gallery view HTML document
def writeGalleryPage(data):
	f = open('portfolio.template', 'r')
	html = f.read()
	f.close()

	gallery_html = ""
	for d in data:
		gallery_html += d["html1"]

	html = html.replace('REPLACE_GALLERY', gallery_html)

	f = open('portfolio.html', 'w')
	f.write(html)
	f.close()

# Writes a new HTML document for one specific artwork
def writePiecePage(d):
	fname = 'pieces/' + str(d['id']) + '.html'

	f = open('artwork.template', 'r')
	html = f.read()
	f.close()

	html = html.replace('REPLACE_TITLE', 'Art piece #' + str(d["id"]))
	html = html.replace('REPLACE_DATE', str(d['dom']) + '.' + str(d['mon']) + '.' + str(d['year']))

	license = '<p>This work is licensed under a</p> <a href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License.</a></p>'
	license += '<img class="licenseimage" id="license" src="/by-nc.png"></img>'

	if 'info' in d:
		html = html.replace('REPLACE_DESCRIPTION', d['info']['description'])
		if 'license' in d['info']:
			if d['info']['license'] == "copyleft":
				pass
			elif d['info']['license'] == "copyright":
				license= '<p>Copyright &copy; ' + str(d['year']) + ' Jesse Kaukonen / Farstrider Oy. All rights reserved.</p>'
	else:
		html = html.replace('REPLACE_DESCRIPTION', '')

	html = html.replace('REPLACE_LICENSE', license)

	link = 'https://plantmonster.net/art/' + d['filename']
	html = html.replace('REPLACE_DATA', '<a href="' + link + '"><img src="' + link + '"></img></a>')

	f = open(fname, 'w')
	f.write(html)
	f.close()

parsedFiles = []
for f in list2:
	d = parseFile(f)
	if d != None:
		parsedFiles.append(d)

for f in parsedFiles:
	formEntry(f)

parsedFiles.sort(key=lambda it: it["id"], reverse=True)
writeGalleryPage(parsedFiles)
for d in parsedFiles:
	writePiecePage(d)
