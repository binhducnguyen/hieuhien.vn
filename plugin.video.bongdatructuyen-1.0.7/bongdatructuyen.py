
import urllib, urllib2, re, os, sys
from bs4 import BeautifulSoup
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui

homelink = 'http://www.bongdatructuyen.vn'
playwire_base_url='http://cdn.playwire.com/'
mysettings = xbmcaddon.Addon(id='plugin.video.bongdatructuyen')
home = mysettings.getAddonInfo('path')
logo = 'http://www.bongdatructuyen.vn/images/logos/114x114.png'
sopcast_logo = 'https://pbs.twimg.com/profile_images/450217704297725952/dz8tA2Nf.png'
acestream_logo = 'http://www.droidsticks.co.uk/wp-content/uploads/2014/05/torrent_stream_logo-300x262.png'

def home():
    try:
        addDir('live','http://www.bongdatructuyen.vn/truc-tiep',4,logo)
        addDir('video','http://www.bongdatructuyen.vn/video',1,logo)
        addDir('Channels',homelink,6,logo)
    except:pass

def getStoredSearch():
    try:
        searches = mysettings.getSetting('store_searches')
        if len(searches)==0:
            searches="[('not a channel',' ')]"
        return searches
    except:pass

def saveStoredSearch(param):
    try:
        mysettings.setSetting('store_searches',repr(param))
    except:pass

def getStoreChannels(url):
    if mysettings.getSetting('save_search')=='true':
        channels =eval(getStoredSearch())
        for chname, chlink in channels:
            title = chname
            link = chlink
            if link!=' ':
                if link.find('sopcast')!=-1:
                    player = 'sopcasts'
                    colorize = '[COLOR FF00BFFF]Sopcast: [/COLOR]'
                elif link.find('acestream')!=-1:
                    player = 'acestreams'
                    colorize = '[COLOR FFFF4500]AceStream: [/COLOR]'
                addLink(colorize+title,link,3,player,logo)


def index_live(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','')
        match = re.compile('<div id="gamesList">(.+?)<div id="footer"').findall(newlink)
        soup = BeautifulSoup(match[0].replace('\t',''))
        games = soup('ul',{'class':'games'})
        for g in games:
            li = BeautifulSoup(str(g))('li')
            for i in li:
                lilink =homelink+str(BeautifulSoup(str(i))('a')[0]['href'])
                licname =BeautifulSoup(str(i))('div',{'class':'cname'})[0].contents[0]
                # licname = str(licname[0:3])
                litime =BeautifulSoup(str(i))('div',{'class':'hour'})[0].contents[0]
                lititle =licname+': '+BeautifulSoup(str(i))('h1')[0].contents[0] +' vs '+BeautifulSoup(str(i))('h1')[1].contents[0]+' - '+litime
                addDir(lititle.encode('utf-8'),lilink,5,logo)
    except:pass

def channel_list(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        list_channel = soup('div',{'id':'list-channel'})
        if len(list_channel)>0:
            li = BeautifulSoup(str(list_channel[0]))('li')
            for i in li:
                lilink = BeautifulSoup(str(i))('a')[0]['href']
                lititle =BeautifulSoup(str(i))('a')[0].contents[0].encode('utf-8')
                if str(lilink).find('sopcast')!=-1:#or str(lilink).find('acestream')!=-1:
                    addLink('sopcasts - '+lititle,lilink,3,'sopcasts',sopcast_logo)
                    update_channels(lititle,lilink)
                elif str(lilink).find('acestream')!=-1:
                    addLink('acestreams - '+lititle,lilink,3,'acestreams',acestream_logo)
                    update_channels(lititle,lilink)
                elif str(lilink).find('sctv')!=-1:
                    addLink(lititle+ ' - sctv',homelink+str(lilink),3,'sctv',homelink+liimage)
        else:
            message = soup('div',{'class':'game-msg'})[0].contents[0]+' [COLOR FF32CD32]'+soup('div',{'class':'game-msg'})[0].next.next.next+' [/COLOR]'+soup('div',{'class':'game-msg'})[0].next.next.next.next
            addLink(message.encode('utf-8'),'',3,'','')

    except:pass
def update_channels(title,link):
    try:
        if mysettings.getSetting('save_search')=='true':
            searches = getStoredSearch()
            searches = eval(searches)
            # idx = 0
            if title!='':
                for i in range(0,len(searches)):
                    cname,llink = searches[i]
                    chname_link = [(title,link)]
                    if title!=cname:
                        searches = chname_link+searches
                        break
                    elif title==cname and link!=llink:
                        searches[i]=(title,link)
                        break
                saveStoredSearch(searches)
    except:pass

def index_video(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        list_videos = soup('div',{'id':'list-videos'})
        li = BeautifulSoup(str(list_videos[0]))('li')
        for i in li:
            alink =homelink + str(BeautifulSoup(str(i))('a')[0]['href'])
            aimage = BeautifulSoup(str(i))('img')[0]['src']
            atitle = BeautifulSoup(str(i))('img')[0]['alt']
            addDir(atitle.encode('utf-8'),alink,2,aimage)
        pager_links = soup('a',{'class':'pager_links'})
        for p in pager_links:
            plink =homelink + str(BeautifulSoup(str(p))('a')[0]['href'])
            ptitle = BeautifulSoup(str(p))('a')[0].contents[0]
            addDir(ptitle.encode('utf-8'),plink,1,logo)
    except:pass

def video_url(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        vurl = str(soup('iframe')[0]['src'])
        newlink = (re.search(r'([a-zA-Z0-9-_]+|.[a-zA-Z0-9-_]+/[a-zA-Z0-9-_]+)(\?v=|/)([a-zA-Z0-9-_]+)',vurl)).group(3)
        addLink(name,newlink,3,'youtube',iconimage)

    except:pass

def rtmp_link(url):
    try:

        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        player = soup('div',{'id':'player'})
        if str(player[0]).find('iframe')==-1:
            filepath = re.compile('file=(.+?)&amp;').findall(link)
            rtmp = re.compile('streamer=(.+?)&amp;').findall(link)
            # vUrl = str(rtmp[0])+ ' swfVfy=1 live=1 playpath='+str(filepath[0])+'flashVer=WIN_11,7,700,202 pageUrl=http://www.tv24.vn tcUrl='+str(rtmp[0])+' swfUrl=http://tv24.vn/jwplayer/player.swf'
            vUrl = str(rtmp[0])+str(filepath[0])
        else:
            iframe_src = BeautifulSoup(str(player[0]))('iframe')[0]['src']
            nlink = urllib2.urlopen(str(iframe_src)).read()
            rtmp = re.compile('file: "(.+?)"').findall(nlink)
            if len(rtmp)<=0:
                rtmp = re.compile("file: '(.+?)'").findall(nlink)

            vUrl = str(rtmp[0])
        return vUrl
    except:pass

def PlayVideo(url):
    try:
        if mirror =='youtube':
            vUrl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid="+urllib.quote_plus(url).replace('?','')
        elif mirror == 'dailymotion':
            vUrl = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url="+urllib.quote_plus(url).replace('?','')
        elif mirror =='picasaweb':
            vUrl = url
        elif mirror =='acestreams':
            vUrl = "plugin://plugin.video.p2p-streams/?mode=1&name="+urllib.quote_plus(name)+"&iconimage="+iconimage+"&url="+urllib.quote_plus(url)
        elif mirror =='sopcasts':
            vUrl = "plugin://plugin.video.p2p-streams/?mode=2&name="+urllib.quote_plus(name)+"&iconimage="+iconimage+"&url="+urllib.quote_plus(url)
        elif mirror =='sctv':
            vUrl =rtmp_link(url)
        else:
            vUrl=url
        if mysettings.getSetting('descriptions')=='true':
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=vUrl))
        else:
            listitem = xbmcgui.ListItem(name,iconImage='DefaultVideo.png',thumbnailImage=iconimage)
            xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(vUrl,listitem)
    except:pass

def addDir(name, url, mode, iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,mirror,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirror="+urllib.quote_plus(mirror)+"&iconimage="+urllib.quote_plus(iconimage)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name})#, "overlay":6,"watched":False})
    liz.setProperty('mimetype', 'video/x-msvideo')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
    return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

params=get_params()
url=None
name=None
mode=None
mirror=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        mirror=urllib.unquote_plus(params["mirror"])
except:
        pass

sysarg=str(sys.argv[1])

if mode==None or url==None or len(url)<1:
    home()
elif mode==1:
    index_video(url)
elif mode==2:
    video_url(url)
elif mode==3:
    PlayVideo(url)
elif mode==4:
    index_live(url)
elif mode==5:
    channel_list(url)
elif mode==6:
    getStoreChannels(url)
xbmcplugin.endOfDirectory(int(sysarg))
