
import re, string, datetime, operator

####################################################################################################

VIDEO_PREFIX = "/video/globalnewsca"

NAME = L('Title')

ART             = 'art-default.jpg'
ICON            = 'icon-default.png'
NATIONAL_ICON   = 'icon-national.png'
BC_ICON         = 'icon-BC.png'
CGY_ICON        = 'icon-CGY.png'
EDM_ICON        = 'icon-EDM.png'
LETH_ICON       = 'icon-LETH.png'
SAS_ICON        = 'icon-SAS.png'
REG_ICON        = 'icon-REG.png'
WIN_ICON        = 'icon-WIN.png'
MON_ICON        = 'icon-MON.png'
TOR_ICON        = 'icon-TOR.png'
MAR_ICON        = 'icon-MAR.png'
CHBC_ICON       = 'icon-CHBC.png'

NATIONAL_PARAMS     = ["z/Global%20Player%20-%20The%20National%20VC", "GLOBNAVC/", "global_nat.com"]
GLOBALNEWS_PARAMS   = ["z/Global%20News%20Player%20-%20Main", "GNEWSVC/", "global_news.com"]
GLOBALBC_PARAMS     = ["z/Global%20BC%20Player%20-%20Video%20Center", "GLBCVC/", "global_bc.com"]
GLOBALCGY_PARAMS    = ["z/Global%20CGY%20Player%20-%20Video%20Center", "GLCGVC/", "global_cal.com"]
GLOBALEDM_PARAMS    = ["z/Global%20EDM%20Player%20-%20Video%20Center", "GLEDVC/", "global_edm.com"]
GLOBALLTH_PARAMS    = ["z/Global%20LTH%20Player%20-%20Video%20Center", "GLLTVC/", "global_lethbridge.com"]
GLOBALSAS_PARAMS    = ["z/Global%20SAS%20Player%20-%20Video%20Center", "GLSAVC/", "global_sas.com"]
GLOBALREG_PARAMS    = ["z/Global%20REG%20Player%20-%20Video%20Center", "GLREVC/", "global_reg.com"]
GLOBALWIN_PARAMS    = ["z/Global%20WIN%20Player%20-%20Video%20Center", "GLWIVC/", "global_win.com"]
GLOBALMON_PARAMS    = ["z/Global%20QC%20Player%20-%20Video%20Center", "GLQCVC/", "global_que.com"]
GLOBALTO_PARAMS     = ["z/Global%20ON%20Player%20-%20Video%20Center", "GLONVC/", "global_ont.com"]
GLOBALMAR_PARAMS    = ["z/Global%20MAR%20Player%20-%20Video%20Center", "GLMAVC/", "global_maritimes.com"]
CHBC_PARAMS         = ["z/CHBC%20Player%20-%20Main", "CHBCNEWS/", "global_nat.com"]

FEED_LIST    = "http://feeds.theplatform.com/ps/JSON/PortalService/2.2/getCategoryList?PID=M3FYkz1jcJIVtzmoB4e_ZQfqBdpZSFNM&startIndex=1&endIndex=500&query=hasReleases&query=CustomText|PlayerTag|%s&field=airdate&field=fullTitle&field=author&field=description&field=PID&field=thumbnailURL&field=title&contentCustomField=title&field=ID&field=parent"

FEEDS_LIST    = "http://feeds.theplatform.com/ps/JSON/PortalService/2.2/getReleaseList?field=ID&field=contentID&field=PID&field=URL&field=categoryIDs&field=length&startIndex=1&endIndex=50&sortField=airdate&PID=M3FYkz1jcJIVtzmoB4e_ZQfqBdpZSFNM&query=Categories|%s&param=Site|%s&query=CategoryIDs|%s&sortDescending=true&field=thumbnailURL&field=title&field=length&field=description&field=airdate"

DIRECT_FEED = "http://release.theplatform.com/content.select?format=SMIL&pid=%s&UserName=Unknown&Embedded=True&TrackBrowser=True&Tracking=True&TrackLocation=True"

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "List"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    
    HTTP.CacheTime = CACHE_1HOUR

####################################################################################################

def VideoMainMenu():

    dir = MediaContainer(viewGroup="List")

    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global National", thumb=R(NATIONAL_ICON)), network = NATIONAL_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global News", thumb=R(ICON)), network = GLOBALNEWS_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global BC", thumb=R(BC_ICON)), network = GLOBALBC_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Calgary", thumb=R(CGY_ICON)), network = GLOBALCGY_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Edmonton", thumb=R(EDM_ICON)), network = GLOBALEDM_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Lethbridge", thumb=R(LETH_ICON)), network = GLOBALLTH_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Saskatoon", thumb=R(SAS_ICON)), network = GLOBALSAS_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Regina", thumb=R(REG_ICON)), network = GLOBALREG_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Winnipeg", thumb=R(WIN_ICON)), network = GLOBALWIN_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Montreal", thumb=R(MON_ICON)), network = GLOBALMON_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Toronto", thumb=R(TOR_ICON)), network = GLOBALTO_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "Global Maritimes", thumb=R(MAR_ICON)), network = GLOBALMAR_PARAMS))
    dir.Append(Function(DirectoryItem(GlobalNewsPage, "CHBC Kelowna", thumb=R(CHBC_ICON)), network = CHBC_PARAMS))
    
    return dir

####################################################################################################

def VideoPlayer(sender, pid):
    videosmil = HTTP.Request(DIRECT_FEED % pid).content
    player = videosmil.split("ref src")
    player = player[2].split('"')
    #Log(player)
    if ".mp4" in player[1]:
        player = player[1].replace(".mp4", "")
        try:
            clip = player.split(";")
            clip = "mp4:" + clip[4]
        except:
            clip = player.split("/video/")
            player = player.split("/video/")[0]
            clip = "mp4:/video/" + clip[-1]
    else:
        player = player[1].replace(".flv", "")
        try:
            clip = player.split(";")
            clip = clip[4]
        except:
            clip = player.split("/video/")
            player = player.split("/video/")[0]
            clip = "/video/" + clip[-1]
    #Log(player)
    #Log(clip)
    return Redirect(RTMPVideoItem(player, clip))

####################################################################################################

def VideosPage(sender, id, network):

    dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList", art=sender.art)
    pageUrl = FEEDS_LIST % (network[0], network[2], id)
    feeds = JSON.ObjectFromURL(pageUrl)
    #Log(feeds)

    for item in feeds['items']:
        title = item['title']
        pid = item['PID']
        summary =  item['description'].replace('In Full:', '')
        duration = item['length']
        thumb = item['thumbnailURL']
        airdate = int(item['airdate'])/1000
        subtitle = 'Originally Aired: ' + datetime.datetime.fromtimestamp(airdate).strftime('%a %b %d, %Y')
        dir.Append(Function(VideoItem(VideoPlayer, title=title, subtitle=subtitle, summary=summary, thumb=thumb, duration=duration), pid=pid))
    
    return dir

####################################################################################################

def GlobalNewsPage(sender, network):
    dir = MediaContainer(title2=sender.itemTitle, viewGroup="List")
    content = JSON.ObjectFromURL(FEED_LIST % network[0])
    showList = {}
    #Log(content)
    items = content['items']
    items.sort(key=operator.itemgetter('fullTitle'))
    #Log(content)
    for item in items:
        if network[1] in item['fullTitle']:
            title = item['fullTitle']
            title = title.split('/')[1]
            #Log(title)
            id = item['ID']
            try:
                if showList[title]:
                    #Log('showList contains %s' % title)
                    discard = dir.Pop(-1)
                    #Log('Removed: %s' %discard.title)
                    dir.Append(Function(DirectoryItem(SeasonsPage, title, thumb=sender.thumb), network=network))
                    showList[title] = {'id':''}
                    #Log('Extra menu level added for %s' % title)
                else:
                    pass
            except:
                #Log('try failed')
                #Log('showList does not contain %s' % title)
                showList[title] = {'id':id}
                dir.Append(Function(DirectoryItem(VideosPage, title), id=id, network=network))
                #Log(showList)
                #Log("Menu entry added for %s" % title)
    return dir
    
####################################################################################################

def SeasonsPage(sender, network):
    dir = MediaContainer(title2=sender.itemTitle, viewGroup="List", art=sender.art)
    content = JSON.ObjectFromURL(FEED_LIST % network[0])
    #Log(sender.itemTitle)
    #Log(content)
    for item in content['items']:
        if sender.itemTitle in item['fullTitle']:
            title = item['fullTitle']
            #Log(title)
            title = title.split('/')[-1]
            id = item['ID']
            #thumb = item['thumbnailURL']
            dir.Append(Function(DirectoryItem(VideosPage, title, thumb=sender.thumb), id=id, network=network))
    dir.Sort('title')
    return dir
            
####################################################################################################