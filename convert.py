#!/usr/bin/python
##### This will convert files from md to html
##############################################

import sys
import re
import yaml
import os
import datetime
import jinja2
import codecs
import distutils.core

## Custom Classes
from bcClasses.posts import Post

def to_unicode_or_bust(obj, encoding='utf-8'):
  if isinstance(obj, basestring):
    if not isinstance(obj, unicode):
      obj = unicode(obj, encoding)
  return obj

def parseFile(filename):
  ''' Open post markdown file and seperate yaml config header from post '''
  meta = 0
  metadata = ""
  mddata = ""
  ## Meta YAML Regex
  reg = re.compile(r'^---$')

  fh = codecs.open(filename, encoding="utf-8", mode="r")
  for line in fh.readlines():
    if reg.search(line) and meta == 0:
      meta = 1
    elif not reg.search(line) and meta == 1:
      metadata = metadata + line
    elif reg.search(line) and meta == 1:
      meta = 0
    elif "[hr]" in line:
      pass
    elif not reg.search(line) and meta == 0:
      mddata = mddata + line
  fh.close()
  to_unicode_or_bust(mddata)
  

  return metadata, mddata

def createFile(path, filename, output):
  ''' Generic Function to Create and write a file '''
  if not os.path.isdir(path):
    os.makedirs(path)
  
  fh = codecs.open(filename, encoding="utf-8", mode="w")
  fh.write(output)
  fh.close()

def genPostPage(f, data, output_dir):
  ''' Create HTML Page for Individual Post '''
  templateLoader = jinja2.FileSystemLoader( searchpath="/" )
  templateEnv = jinja2.Environment( loader=templateLoader )
  template = templateEnv.get_template(f)
  tempVars = { 'data' : data }
  outputText = template.render( tempVars )
  outputText.encode('utf-8')

  ## Create year/month/date/slug/index.html
  filedir = output_dir + "/" + data['url']
  filename = output_dir + "/" + data['url'] + "/index.html"
  createFile(filedir, filename, outputText)

  ## Create year/month/slug/index.html
  filedir = output_dir + "/" + data['url2']
  filename = output_dir + "/" + data['url2'] + "/index.html"
  createFile(filedir, filename, outputText)

  return True

def genIndexPage(f, data, output_dir):
  ''' Create HTML Page for Inddex Page '''
  templateLoader = jinja2.FileSystemLoader( searchpath="/" )
  templateEnv = jinja2.Environment( loader=templateLoader )
  template = templateEnv.get_template(f)
  tempVars = { 'data' : data }
  outputText = template.render( tempVars )
  outputText.encode('utf-8')
  ## Create year/month/slug/index.html
  filedir = output_dir + "/" 
  filename = output_dir + "/index.html"
  createFile(filedir, filename, outputText)
  return True
      

def genPage(f, tf, data, output_dir):
  ''' Create HTML Page for Archive Page '''
  templateLoader = jinja2.FileSystemLoader( searchpath="/" )
  templateEnv = jinja2.Environment( loader=templateLoader )
  template = templateEnv.get_template(tf)
  tempVars = { 'data' : data }
  outputText = template.render( tempVars )
  outputText.encode('utf-8')
  ## Create year/month/slug/index.html
  filedir = output_dir + "/" 
  filename = output_dir + "/" + f
  createFile(filedir, filename, outputText)

  return True



## Config file
if len(sys.argv) != 3:
  print("Hey! that's not how you call this!")
  print("Usage: %s -c <configfile>") % sys.argv[0]
  sys.exit(1)
else:
  configfile = sys.argv[2]

## Open Config File and Parse Config Data
cfh = open(configfile, "r")
config = yaml.safe_load(cfh)
cfh.close()

## Start Working with posts
posts = {}
pids = []
rpids = []

print "Opening files in the %s directory" % config['post_dir']
print "-" * 10
for files in os.listdir(config['post_dir']):
  if files.endswith(".markdown"):
    metadata, mddata = parseFile(config['post_dir'] + "/" + files)
    post = Post(metadata, mddata)

    posts[post.pid] = post
    pids.append(post.pid)
    rpids.append(post.pid)
    print "Finished with post %d" % post.pid

print "#" * 10

## Sort the index of pids
pids.sort()
rpids.sort()
rpids.reverse()

## Setup Next and Previous URL's
runnum = 0
plen = len(pids)
print "Setting up next and previous post links, This will spam your screen."
print "-" * 10
for key in pids:
  pnum = runnum - 1
  nnum = runnum + 1
  print "working on item: " + str(runnum) + " - " + posts[key].url
  if not runnum == 0:
    print "checking " + str(pnum)
    if pids[pnum]:
      posts[key].prevp = posts[pids[pnum]].url

  print "Prev Post " + str(pnum) + ": ",
  print posts[key].prevp

  if nnum < plen:
    print "checking " + str(nnum) 
    if pids[nnum]:
      posts[key].nextp = posts[pids[nnum]].url

  print "Next Post " + str(nnum) + ": ",
  print posts[key].nextp
  print ""
  print "-" * 10
  print ""

  runnum = runnum + 1

print "#" * 10

## Create HTML Files
runnum = 0
plen = len(pids)

allposts = {}

for key in pids:
  print "Starting with post %s" % posts[key].title
  htmldata = {}
  htmldata['sitename'] = config['site_name']
  htmldata['author'] = config['site_author']
  htmldata['authorlink'] = config['site_authorlink']
  htmldata['pagetype'] = "article"
  htmldata['siteurl'] = config['site_url']
  htmldata['sitefeed'] = config['site_feed']
  
  
  htmldata['title'] = posts[key].title
  htmldata['sitetitle'] = posts[key].title
  htmldata['description'] = posts[key].description
  if posts[key].description:
    htmldata['sitedescription'] = posts[key].description
  else:
    htmldata['sitedescription'] = None

  if posts[key].thumbnail:
    htmldata['thumbnail'] = posts[key].thumbnail
  else:
    htmldata['thumbnail'] = config['site_thumbnail']
  htmldata['date'] = posts[key].date
  htmldata['pubdate'] = posts[key].pubdate
  htmldata['data'] = posts[key].posthtml
  htmldata['url'] = posts[key].url
  htmldata['url2'] = posts[key].url2
  htmldata['prevp'] = posts[key].prevp
  htmldata['nextp'] = posts[key].nextp
  htmldata['tochtml'] = posts[key].tochtml
  htmldata['toccount'] = posts[key].toccount
  htmldata['cats'] = posts[key].cats
  htmldata['tags'] = posts[key].tags
  htmldata['popularity'] = posts[key].popularity
  if runnum == plen - 1:
    htmldata['lastpost'] = True
  else:
    htmldata['lastpost'] = False 

  runnum = runnum + 1
  allposts[key] = htmldata
  
  template = config['template_dir'] + "/" + config['templates']['post']
  if genPostPage(template, htmldata, config['output_dir']):
    print "Post id %d created" % posts[key].pid
  else:
    print "Post id %d not created" % posts[key].pid

  if htmldata['lastpost']:
    htmldata['sitetitle'] = config['site_name'] + " | " + config['site_shortdesc']
    htmldata['siteurl'] = config['site_url']
    htmldata['sitefeed'] = config['site_feed']
    htmldata['sitedescription'] = config['site_description']
    htmldata['tags'] = config['site_keywords']
    htmldata['cats'] = []
    htmldata['pagetype'] = "blog"

    template = config['template_dir'] + "/" + config['templates']['post']
    if genIndexPage(template, htmldata, config['output_dir']):
      print "Post id %d created as Index" % posts[key].pid
    else:
      print "Post id %d not created" % posts[key].pid
    
## Generate Archive Page 
htmldata = {}
htmldata['sitename'] = config['site_name']
htmldata['author'] = config['site_author']
htmldata['authorlink'] = config['site_authorlink']
htmldata['author'] = config['site_author']
htmldata['sitetitle'] = config['site_name'] + " | Archive"
htmldata['siteurl'] = config['site_url']
htmldata['sitefeed'] = config['site_feed']
htmldata['url'] = config['site_url'] + "/archive.html"
htmldata['sitedescription'] = config['site_description']
htmldata['tags'] = config['site_keywords']
htmldata['cats'] = []
htmldata['pagetype'] = "blog"
htmldata['rowitems'] = allposts
htmldata['rpids'] = rpids

template = config['template_dir'] + "/" + config['templates']['archive']
if genPage("archive.html", template, htmldata, config['output_dir']):
  print "Created a Archive"
else:
  print "Could not create an Archive"

htmldata['siteurl'] = config['site_url']
htmldata['sitefeed'] = config['site_feed']

template = config['template_dir'] + "/" + config['templates']['sitemap']
if genPage("sitemap.xml", template, htmldata, config['output_dir']):
  print "Created a Sitemap"
else:
  print "Could not create a Sitemap"

## Generate RSS Page 
htmldata = {}
htmldata['sitename'] = config['site_name']
htmldata['author'] = config['site_author']
htmldata['description'] = config['site_description']
htmldata['sitetitle'] = config['site_name']
htmldata['siteurl'] = "http://bencane.com"
htmldata['sitefeed'] = config['site_feed']
htmldata['pagetype'] = "rss"
htmldata['rowitems'] = allposts
htmldata['rpids'] = rpids[:10]

template = config['template_dir'] + "/" + config['templates']['feed']
if genPage("index.xml", template, htmldata, config['output_dir'] + "/feed"):
  print "Created a RSS Feed"
else:
  print "Could not create an RSS Feed"

htmldata['rowtitle'] = "Recent Posts"
htmldata['sitedescription'] = config['site_name'] + " | 404 Not Found"

template = config['template_dir'] + "/" + config['templates']['notfound']
if genPage("404.html", template, htmldata, config['output_dir'] ):
  print "Created a 404 Page"
else:
  print "Could not create a 404 Page "

htmldata['rowtitle'] = "Recent Posts"
htmldata['sitedescription'] = config['site_name'] + " | 403 Forbidden"

template = config['template_dir'] + "/" + config['templates']['forbidden']
if genPage("403.html", template, htmldata, config['output_dir'] ):
  print "Created a 403 Page"
else:
  print "Could not create a 403 Page "

## Copy CSS
distutils.dir_util.copy_tree(config['static_dir'], config['output_dir'] + "/static")
