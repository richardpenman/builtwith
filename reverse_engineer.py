import sys
import re
import urllib2


def reverse_engineer(url, headers=None, html=None, user_agent='reverse_engineer'):
    """Detect the technology used by a website

    >>> reverse_engineer('http://wordpress.com') == {'Blog': 'WordPress', 'JavaScript framework': 'jQuery', 'CMS': 'WordPress', 'Web server': 'Nginx'}
    True
    >>> reverse_engineer('http://sitescraper.net') == {'Analytics': 'Google Analytics', 'Web server': 'Nginx'}
    True

    """
    technology = {}

    # check URL
    for app_name, app_spec in apps.items():
        if 'url' in app_spec:
            if re.compile(app_spec['url'], re.IGNORECASE).search(url):
                for category in get_categories(app_spec):
                    technology[category] = app_name

    # download content
    if None in (headers, html):
        try:
            request = urllib2.Request(url, None, {'User-Agent': user_agent})
            if html:
                # already have HTML so just need to make HEAD request for headers
                request.get_method = lambda : 'HEAD'
            response = urllib2.urlopen(request)
            if headers is None:
                headers = response.headers
            if html is None:
                html = response.read()
        except Exception, e:
            print 'Error:', e
            request = None

    # check headers
    if headers:
        for app_name, app_spec in apps.items():
            if 'headers' in app_spec:
                if contains_dict(headers, app_spec['headers']):
                    for category in get_categories(app_spec):
                        technology[category] = app_name
                    break

    # check html
    if html:
        for app_name, app_spec in apps.items():
            for key in 'html', 'script':
                if key in app_spec:
                    if re.compile(app_spec[key], re.IGNORECASE).search(html):
                        for category in get_categories(app_spec):
                            technology[category] = app_name

        # check meta
        # XXX add proper meta data parsing
        contents = re.compile('<meta.*?content=[\'"]?(.*?)[\'"].*?>', re.IGNORECASE).findall(html)
        for app_name, app_spec in apps.items():
            generator = app_spec.get('meta', {}).get('generator')
            if generator:
                for content in contents:
                    if re.compile(generator, re.IGNORECASE).match(content):
                        for category in get_categories(app_spec):
                            technology[category] = app_name

                
    return technology



def get_categories(app_spec):
    """Return category names for this app_spec
    """
    return [categories[c_id] for c_id in app_spec['cats']]

def contains_dict(d1, d2):
    """Takes 2 dictionaries
    
    Returns True if d1 contains all items in d2"""
    for k2, v2 in d2.items():
        v1 = d1.get(k2)
        if v1:
            if not re.compile(v2, re.IGNORECASE).search(v1):
                return False
        else:
            return False
    return True



# these lists were adapted from Wappalyzer (https://github.com/ElbertF/Wappalyzer)
categories = {
     1: 'CMS',
     2: 'Message Board',
     3: 'Database manager',
     4: 'Documentation tool',
     5: 'Widget',
     6: 'Web shop',
     7: 'Photo gallery',
     8: 'Wiki',
     9: 'Hosting panel',
    10: 'Analytics',
    11: 'Blog',
    12: 'JavaScript framework',
    13: 'Issue tracker',
    14: 'Video Player',
    15: 'Comment System',
    16: 'CAPTCHA',
    17: 'Font script',
    18: 'Web framework',
    19: 'Miscellaneous',
    20: 'Editor',
    21: 'LMS',
    22: 'Web server',
    23: 'Cache tool',
    24: 'Rich text editor',
    25: 'Javascript graphics',
    26: 'Mobile framework',
}

apps = {
    '1C-Bitrix':             {'cats': [1], 'html': '<link[^>]+components\/bitrix', 'script': '1c\-bitrix/' },
    '2z Project':            {'cats': [1], 'meta': { 'generator': '2z project' } },
    'AddThis':               {'cats': [5], 'script': 'addthis\.com\/js' },
    'Adobe GoLive':          {'cats': [20], 'meta': { 'generator': 'Adobe GoLive' } },
    'Advanced Web Stats':    {'cats': [10], 'html': 'aws.src = [^<]+caphyon\-analytics' },
    'Amiro.CMS':             {'cats': [1], 'meta': { 'generator': 'Amiro' } },
    'Apache':                {'cats': [22], 'headers': { 'Server': 'Apache' } },
    'Apache Tomcat':         {'cats': [22], 'headers': { 'Server': 'Apache-Coyote' } },
    'Atlassian Confluence':  {'cats': [8], 'html': 'Powered by <a href=.http:\/\/www\.atlassian\.com\/software\/confluence' },
    'Atlassian Jira':        {'cats': [13], 'html': 'Powered by <a href=.http:\/\/www\.atlassian\.com\/software\/jira' },
    'AWStats':               {'cats': [10], 'meta': { 'generator': 'AWStats' } },
    'Banshee':               {'cats': [1, 18], 'html': 'Built upon the <a href=("|\')[^>]+banshee-php\.org' },
    'Backbone.js':           {'cats': [12], 'script': 'backbone.*\.js', 'env': '^Backbone$' },
    'BIGACE':                {'cats': [1], 'meta': { 'generator': 'BIGACE' }, 'html': 'Powered by <a href=("|\')[^>]+BIGACE|<!--\s+Site is running BIGACE' },
    'BigDump':               {'cats': [3], 'html': '<!-- <h1>BigDump: Staggered MySQL Dump Importer' },
    'blip.tv':               {'cats': [14], 'html': '<(param|embed)[^>]+blip\.tv\/play' },
    'Blogger':               {'cats': [11], 'meta': { 'generator': 'blogger' }, 'url': '^(www.)?.+\.blogspot\.com' },
    'Bugzilla':              {'cats': [13], 'html': '<[^>]+(id|title|name)=("|\')bugzilla' },
    'Burning Board':         {'cats': [2], 'html': '<a href=(\'|")[^>]+woltlab\.com.+Burning Board' },
    'Chameleon':             {'cats': [1], 'meta': { 'generator': 'chameleon\-cms' } },
    'chartbeat':             {'cats': [10], 'html': 'function loadChartbeat\(\) {' },
    'Chamilo':               {'cats': [21], 'meta': { 'generator': 'Chamilo' }, 'headers': { 'X-Powered-By': 'Chamilo' } },
    'Cherokee':              {'cats': [22], 'headers': { 'Server': 'Cherokee' } },
    'ClickHeat':             {'cats': [10], 'script': 'clickheat.*\.js', 'env': '^clickHeatBrowser$' },
    'ClickTale':             {'cats': [10], 'html': 'if\(typeof ClickTale(Tag)*==("|\')function("|\')\)' },
    'Clicky':                {'cats': [10], 'script': 'static\.getclicky\.com' },
    'CMS Made Simple':       {'cats': [1], 'meta': { 'generator': 'CMS Made Simple' } },
    'CO2Stats':              {'cats': [10], 'html': 'src=("|\')http:\/\/www\.co2stats\.com\/propres\.php' },
    'comScore':              {'cats': [10], 'html': '<i{1}frame[^>]* (id=("|\')comscore("|\')|scr=[^>]+comscore)' },
    'Concrete5':             {'cats': [1], 'meta': { 'generator': 'concrete5' } },
    'Contao':                {'cats': [1], 'html': '(<!--\s+This website is powered by (TYPOlight|Contao)|<link[^>]+(typolight|contao).css)' },
    'Contens':               {'cats': [1], 'meta': { 'generator': 'contens' } },
    'ConversionLab':         {'cats': [10], 'script': 'conversionlab\.trackset\.com\/track\/tsend\.js' },
    'Coppermine':            {'cats': [7], 'html': '<!--Coppermine Photo Gallery' },
    'Cotonti':               {'cats': [1], 'meta': { 'generator': 'Cotonti' } },
    'cPanel':                {'cats': [9], 'html': '<!-- cPanel' },
    'Crazy Egg':             {'cats': [10], 'script': 'cetrk\.com\/pages\/scripts\/[0-9]+\/[0-9]+\.js' },
    'CS Cart':               {'cats': [6], 'html': '&nbsp;Powered by (<a href=.http:\/\/www\.cs\-cart\.com|CS\-Cart)' },
    'CubeCart':              {'cats': [6], 'html': 'Powered by <a href=.http:\/\/www\.cubecart\.com' },
    'cufon':                 {'cats': [17], 'script': 'cufon\-yui\.js', 'env': '^Cufon$' },
    'd3':                    {'cats': [25], 'script': 'd3(\.min)?\.js', 'env': '^d3$' },
    'Danneo CMS':            {'cats': [1], 'meta': { 'generator': 'Danneo' } },
    'DataLife Engine':       {'cats': [1], 'meta': { 'generator': 'DataLife Engine' } },
    'DHTMLX':                {'cats': [12], 'script': 'dhtmlxcommon\.js' },
    'DirectAdmin':           {'cats': [9], 'html': '<a[^>]+>DirectAdmin<\/a> Web Control Panel' },
    'Disqus':                {'cats': [15], 'script': 'disqus_url', 'html': '<div[^>]+id=("|\')disqus_thread("|\')' },
    'dojo':                  {'cats': [12], 'script': 'dojo(\.xd)?\.js', 'env': '^dojo$' },
    'Dokeos':                {'cats': [21], 'meta': { 'generator': 'Dokeos' }, 'html': 'Portal <a[^>]+>Dokeos|@import "[^"]+dokeos_blue', 'headers': { 'X-Powered-By': 'Dokeos' } },
    'DokuWiki':              {'cats': [8], 'meta': { 'generator': 'DokuWiki' } },
    'DotNetNuke':            {'cats': [1], 'meta': { 'generator': 'DotNetNuke' }, 'html': '<!\-\- by DotNetNuke Corporation' },
    'DreamWeaver':           {'cats': [20], 'html': '(<!\-\-[^>]*(InstanceBeginEditable|Dreamweaver[^>]+target|DWLayoutDefaultTable)|function MM_preloadImages\(\) {)' },
    'Drupal':                {'cats': [1], 'script': 'drupal\.js', 'html': '(jQuery\.extend\(Drupal\.settings, \{|Drupal\.extend\(\{ settings: \{|<link[^>]+sites\/(default|all)\/themes\/|<style[^>]+sites\/(default|all)\/(themes|modules)\/)', 'headers': { 'X-Drupal-Cache': '.*', 'Expires': '19 Nov 1978' }, 'env': '^Drupal$' },
    'Drupal Commerce':       {'cats': [6], 'html': 'id\=\"block\-commerce\-cart\-cart|class\=\"commerce\-product\-field' },
    'Dynamicweb':            {'cats': [1], 'meta': { 'generator': 'Dynamicweb' } },
    'e107':                  {'cats': [1], 'script': 'e107\.js' },
    'Exhibit':               {'cats': [25], 'script': 'exhibit.*\.js', 'env': '^Exhibit$' },
    'ExtJS':                 {'cats': [12], 'script': 'ext\-base\.js', 'env': '^Ext$' },
    'ExpressionEngine':      {'cats': [1], 'headers': { 'Set-Cookie': 'exp_last_activity' } },
    'eZ Publish':            {'cats': [1], 'meta': { 'generator': 'eZ Publish' } },
    'FluxBB':                {'cats': [2], 'html': 'Powered by (<strong>)?<a href=("|\')[^>]+fluxbb' },
    'Flyspray':              {'cats': [13], 'html': '(<a[^>]+>Powered by Flyspray|<map id=("|\')projectsearchform)' },
    'FrontPage':             {'cats': [20], 'meta': { 'generator': 'Microsoft FrontPage' }, 'html': '<html[^>]+urn:schemas\-microsoft\-com:office:office' },
    'Get Satisfaction':      {'cats': [13], 'html': 'var feedback_widget = new GSFN\.feedback_widget\(feedback_widget_options\)' },
    'Google Analytics':      {'cats': [10], 'script': '(\.google\-analytics\.com\/ga\.js|google-analytics\.com\/urchin\.js)', 'env': '^gaGlobal$' },
    'Google App Engine':     {'cats': [22], 'headers': { 'Server': 'Google Frontend' } },
    'Google Font API':       {'cats': [17], 'html': '<link[^>]* href=("|\')http:\/\/fonts\.googleapis\.com' },
    'Google Friend Connect': {'cats': [5], 'script': 'google.com\/friendconnect' },
    'Google Maps':           {'cats': [5], 'script': '(maps\.google\.com\/maps\?file=api|maps\.google\.com\/maps\/api\/staticmap)' },
    'Graffiti CMS':          {'cats': [1], 'meta': { 'generator': 'Graffiti CMS' } },
    'Gravity Insights':      {'cats': [10], 'html': 'gravityInsightsParams\.site_guid = ' },
    'Hiawatha':              {'cats': [22], 'headers': { 'Server': 'Hiawatha' } },
    'Highcharts':            {'cats': [25], 'script': 'highcharts.*\.js', 'env': '^Highcharts$' },
    'Hotaru CMS':            {'cats': [1], 'meta': { 'generator': 'Hotaru CMS' } },
    'IIS':                   {'cats': [22], 'headers': { 'Server': 'IIS' } },
    'InstantCMS':            {'cats': [1], 'meta': { 'generator': 'InstantCMS' } },
    'IPB':                   {'cats': [2], 'script': 'jscripts\/ips_' },
    'iWeb':                  {'cats': [20], 'meta': { 'generator': 'iWeb' } },
    'Jalios':                {'cats': [1], 'meta': { 'generator': 'Jalios' } },
    'Javascript Infovis Toolkit': {'cats': [25], 'script': 'jit.*\.js', 'env': '^\$jit$' },
    'Jo':                    {'cats': [26, 12], 'script': '[^a-zA-Z]jo.*\.js' },
    'Joomla':                {'cats': [1], 'meta': { 'generator': 'Joomla' }, 'html': '<!\-\- JoomlaWorks "K2"', 'headers': { 'X-Content-Encoded-By': 'Joomla' } },
    'jqPlot':                {'cats': [25], 'script': 'jqplot.*\.js', 'env': '^jQuery.jqplot$' },
    'jQTouch':               {'cats': [26], 'script': 'jqtouch.*\.js', 'env': '^jQT$' },
    'jQuery UI':             {'cats': [12], 'script': 'jquery\-ui.*\.js' },
    'jQuery':                {'cats': [12], 'script': 'jquery.*.js', 'env': '^jQuery$' },
    'jQuery Mobile':         {'cats': [26], 'script': 'jquery\.mobile.*\.js' },
    'jQuery Sparklines':     {'cats': [25], 'script': 'jquery\.sparkline.*\.js' },
    'JS Charts':             {'cats': [25], 'script': 'jscharts.*\.js', 'env': '^JSChart$' },
    'JTL Shop':              {'cats': [6], 'html': '(<input[^>]+name=("|\')JTLSHOP|<a href=("|\')jtl\.php)' },
    'K2':                    {'cats': [19], 'html': '<!\-\- JoomlaWorks "K2"' },
    'Kampyle':               {'cats': [10], 'script': 'cf\.kampyle\.com\/k_button\.js' },
    'Kentico CMS':           {'cats': [1], 'meta': { 'generator': 'Kentico CMS' } },
    'Koego':                 {'cats': [10], 'script': 'tracking\.koego\.com\/end\/ego\.js' },
    'Kolibri CMS':           {'cats': [1], 'meta': { 'generator': 'Kolibri' } },
    'Koobi':                 {'cats': [1], 'meta': { 'generator': 'Koobi' } },
    'lighttpd':              {'cats': [22], 'headers': { 'Server': 'lighttpd' } },
    'LiveJournal':           {'cats': [11], 'url': '^(www.)?.+\.livejournal\.com' },
    'Lotus Domino':          {'cats': [22], 'headers': { 'Server': 'Lotus\-Domino' } },
    'Magento':               {'cats': [6], 'html': 'var BLANK_URL = \'[^>]+js\/blank\.html' },
    'Mambo':                 {'cats': [1], 'meta': { 'generator': 'Mambo' } },
    'MantisBT':              {'cats': [13], 'html': '<img[^>]+ alt=("|\')Powered by Mantis Bugtracker' },
    'MaxSite CMS':           {'cats': [1], 'meta': { 'generator': 'MaxSite CMS' } },
    'MediaWiki':             {'cats': [8], 'meta': { 'generator': 'MediaWiki' }, 'html': '(<a[^>]+>Powered by MediaWiki<\/a>|<[^>]+id=("|\')t\-specialpages)' },
    'Meebo':                 {'cats': [5], 'html': '(<iframe id=("|\')meebo\-iframe("|\')|Meebo\(\'domReady\'\))' },
    'Microsoft ASP.NET':     {'cats': [18], 'html': '<input[^>]+name=("|\')__VIEWSTATE', 'headers': { 'X-Powered-By': 'ASP\.NET', 'X-AspNet-Version': '.+' } },
    'Microsoft SharePoint':  {'cats': [1], 'meta': { 'generator': 'Microsoft SharePoint' }, 'headers': { 'MicrosoftSharePointTeamServices': '.*', 'X-SharePointHealthScore': '.*', 'SPRequestGuid': '.*' } },
    'MiniBB':                {'cats': [2], 'html': '<a href=("|\')[^>]+minibb.+\s+<!--End of copyright link' },
    'Mint':                  {'cats': [10], 'script': 'mint\/\?js' },
    'Mixpanel':              {'cats': [10], 'script': 'api\.mixpanel\.com\/track' },
    'MochiKit':              {'cats': [12], 'script': 'MochiKit\.js', 'env': '^MochiKit$' },
    'Modernizr':             {'cats': [12], 'script': 'modernizr.*\.js' },
    'MODx':                  {'cats': [1], 'html': '(<a[^>]+>Powered by MODx<\/a>|var el= \$\(\'modxhost\'\);|<script type=("|\')text\/javascript("|\')>var MODX_MEDIA_PATH = "media";)|<(link|script)[^>]+assets\/(templates|snippets)\/' },
    'Mollom':                {'cats': [16], 'script': 'mollom\.js', 'html': '<img[^>]+\/.mollom\/.com' },
    'Moodle':                {'cats': [21], 'html': '(var moodleConfigFn = function\(me\)|<img[^>]+moodlelogo)' },
    'Moogo':                 {'cats': [1], 'script': 'kotisivukone.js' },
    'MooTools':              {'cats': [12], 'script': 'mootools.*\.js', 'env': '^MooTools$' },
    'Movable Type':          {'cats': [1], 'meta': { 'generator': 'Movable Type' } },
    'MyBB':                  {'cats': [2], 'html': '(<script [^>]+\s+<!--\s+lang\.no_new_posts|<a[^>]* title=("|\')Powered By MyBB)' },
    'MyBlogLog':             {'cats': [5], 'script': 'pub\.mybloglog\.com' },
    'Mynetcap':              {'cats': [1], 'meta': { 'generator': 'Mynetcap' } },
    'Nedstat':               {'cats': [10], 'html': 'sitestat\(("|\')http:\/\/nl\.sitestat\.com' },
    'Nginx':                 {'cats': [22], 'headers': { 'Server': 'nginx' } },
    'NOIX':                  {'cats': [19], 'html': '<[^>]+(src|href)=[^>]*(\/media\/noix)|<!\-\- NOIX' },
    'nopCommerce':           {'cats': [6], 'html': '(<!\-\-Powered by nopCommerce|Powered by: <a[^>]+nopcommerce)' },
    'OpenCart':              {'cats': [6], 'html': '(Powered By <a href=("|\')[^>]+OpenCart|route = getURLVar\(("|\')route)' },
    'openEngine':            {'cats': [1], 'html': '<meta[^>]+openEngine' },
    'OpenGSE':               {'cats': [22], 'headers': { 'Server': 'GSE' } },
    'OpenLayers':            {'cats': [5], 'script': 'openlayers', 'env': '^OpenLayers$' },
    'osCommerce':            {'cats': [6], 'html': '<!-- header_eof \/\/-->|<a[^>]*(osCsid|cPath)' },
    'osCSS':                 {'cats': [6], 'html': '<body onload=("|\')window\.defaultStatus=\'oscss templates\';("|\')' },
    'PANSITE':               {'cats': [1], 'meta': { 'generator': 'PANSITE' } },
    'papaya CMS':            {'cats': [1], 'html': '<link[^>]*\/papaya-themes\/' },
    'PHP-Fusion':            {'cats': [1], 'html': 'Powered by <a href=("|\')[^>]+php-fusion' },
    'PHP-Nuke':              {'cats': [2], 'meta': { 'generator': 'PHP-Nuke' }, 'html': '<[^>]+Powered by PHP\-Nuke' },
    'phpBB':                 {'cats': [2], 'meta': { 'copyright': 'phpBB Group' }, 'html': 'Powered by (<a href=("|\')[^>]+)?phpBB' },
    'phpDocumentor':         {'cats': [4], 'html': '<!-- Generated by phpDocumentor' },
    'phpMyAdmin':            {'cats': [3], 'html': '(var pma_absolute_uri = \'|PMA_sendHeaderLocation\(|<title>phpMyAdmin<\/title>)' },
    'phpPgAdmin':            {'cats': [3], 'html': '(<title>phpPgAdmin<\/title>|<span class=("|\')appname("|\')>phpPgAdmin)' },
    'Piwik':                 {'cats': [10], 'html': 'var piwikTracker = Piwik\.getTracker\(' },
    'Plesk':                 {'cats': [9], 'script': 'common\.js\?plesk' },
    'Plone':                 {'cats': [1], 'meta': { 'generator': 'Plone' } },
    'Plura':                 {'cats': [19], 'html': '<iframe src="http:\/\/pluraserver\.com' },
    'posterous':             {'cats': [1, 11], 'html': '<div class=("|\')posterous' },
    'Prestashop':            {'cats': [6], 'meta': { 'generator': 'PrestaShop' }, 'html': 'Powered by <a href=("|\')[^>]+PrestaShop' },
    'Prototype':             {'cats': [12], 'script': '(prototype|protoaculous)\.js', 'env': '^Prototype$' },
    'Protovis':              {'cats': [25], 'script': 'protovis.*\.js', 'env': '^protovis$' },
    'punBB':                 {'cats': [2], 'html': 'Powered by <a href=("|\')[^>]+punbb' },
    'Quantcast':             {'cats': [10], 'script': 'edge\.quantserve\.com\/quant\.js', 'env': '^quantserve$' },
    'Quick.Cart':            {'cats': [6], 'html': '<a href="[^>]+opensolution\.org\/">Powered by' },
    'Raphael':               {'cats': [25], 'script': 'raphael.*\.js', 'env': '^Raphael$' },
    'reCAPTCHA':             {'cats': [16], 'script': '(api\-secure\.recaptcha\.net|recaptcha_ajax\.js)', 'html': '<div[^>]+id=("|\')recaptcha_image' },
    'Reddit':                {'cats': [2], 'html': '(<script[^>]+>var reddit = {|<a[^>]+Powered by Reddit|powered by <a[^>]+>reddit<)', 'url': '^(www.)?reddit\.com' },
    'Redmine':               {'cats': [13], 'meta': { 'description': 'Redmine' }, 'html': 'Powered by <a href=("|\')[^>]+Redmine' },
    'Reinvigorate':          {'cats': [10], 'html': 'reinvigorate\.track\("' },
    'RequireJS':             {'cats': [12], 'script': 'require.*\.js', 'env': '^requirejs$'},
    'S.Builder':             {'cats': [1], 'meta': { 'generator': 'S\.Builder' } },
    's9y':                   {'cats': [1], 'meta': { 'generator': 'Serendipity' } },
    'script.aculo.us':       {'cats': [12], 'script': '(scriptaculous|protoaculous)\.js', 'env': '^Scriptaculous$' },
    'Sencha Touch':          {'cats': [26, 12], 'script': 'sencha\-touch.*\.js' },
    'ShareThis':             {'cats': [5], 'script': 'w\.sharethis\.com\/' },
    'sIFR':                  {'cats': [17], 'script': 'sifr\.js' },
    'Site Meter':            {'cats': [10], 'script': 'sitemeter.com\/js\/counter\.js\?site=' },
    'SiteCatalyst':          {'cats': [10], 'html': 'var s_code=s\.t\(\);if\(s_code\)document\.write\(s_code\)' },
    'SiteEdit':              {'cats': [1], 'meta': { 'generator': 'SiteEdit' } },
    'SMF':                   {'cats': [2], 'html': '<script [^>]+\s+var smf_' },
    'sNews':                 {'cats': [1], 'meta': { 'generator': 'sNews' } },
    'Snoobi':                {'cats': [10], 'script': 'snoobi\.com\/snoop\.php' },
    'SOBI 2':                {'cats': [19], 'html': '(<!\-\- start of Sigsiu Online Business Index|<div[^>]* class=("|\')sobi2)' },
    'SPIP':                  {'cats': [1], 'meta': { 'generator': 'SPIP' }, 'headers': { 'X-Spip-Cache': '.*' } },
    'SQL Buddy':             {'cats': [3], 'html': '(<title>SQL Buddy<\/title>|<[^>]+onclick=("|\')sideMainClick\(("|\')home\.php)' },
    'Squarespace':           {'cats': [1], 'html': 'Squarespace\.Constants\.CURRENT_MODULE_ID' },
    'Squiz Matrix':          {'cats': [1], 'meta': { 'generator': 'Squiz Matrix' }, 'html': '  Running (MySource|Squiz) Matrix', 'X-Powered-By': 'Squiz Matrix' },
    'StatCounter':           {'cats': [10], 'script': 'statcounter\.com\/counter\/counter' },
    'SWFObject':             {'cats': [19], 'script': 'swfobject.*\.js' },
    'swift.engine':          {'cats': [1], 'headers': { 'X-Powered-By': 'swift\.engine' } },
    'Swiftlet':              {'cats': [1, 18], 'meta': { 'generator': 'Swiftlet' }, 'html': 'Powered by <a href=("|\')[^>]+Swiftlet', 'headers': { 'X-Swiftlet-Cache': '.*', 'X-Powered-By': 'Swiftlet' } },
    'Textpattern CMS':       {'cats': [1], 'meta': { 'generator': 'Textpattern' } },
    'Timeline':              {'cats': [25], 'script': 'timeline.*\.js', 'env': '^Timeline$' },
    'Timeplot':              {'cats': [25], 'script': 'timeplot.*\.js', 'env': '^Timeplot$' },
    'TomatoCart':            {'cats': [6], 'meta': { 'generator': 'TomatoCart' } },
    'Trac':                  {'cats': [13], 'html': '(<a id=("|\')tracpowered)' },
    'Tumblr':                {'cats': [11], 'html': '<iframe src=("|\')http:\/\/www\.tumblr\.com', 'url': '^(www.)?.+\.tumblr\.com', 'headers': { 'X-Tumblr-Usec': '.*' } },
    'Twilight CMS':          {'cats': [1], 'headers': { 'X-Powered-CMS': 'Twilight CMS' } },
    'Typekit':               {'cats': [17], 'script': 'use.typekit.com', 'env': '^Typekit$' },
    'TypePad':               {'cats': [11], 'meta': { 'generator': 'typepad' }, 'url': '^(www.)?.+\.typepad\.com' },
    'TYPO3':                 {'cats': [1], 'meta': { 'generator': 'TYPO3' }, 'html': '(<(script[^>]* src|link[^>]* href)=[^>]*fileadmin)', 'url': '\/typo3', 'version': 'content="TYPO3 (.*?) CMS"' },
    'Ubercart':              {'cats': [6], 'script': 'uc_cart\/uc_cart_block\.js' },
    'Umbraco':               {'cats': [1], 'headers': { 'X-Umbraco-Version': '.+' } },
    'Underscore.js':         {'cats': [12], 'script': 'underscore.*\.js' },
    'UserRules':             {'cats': [13], 'html': 'var _usrp =' , 'env': '^\_usrp$' },
    'Vanilla':               {'cats': [2], 'html': '<body id=("|\')(DiscussionsPage|vanilla)', 'headers': { 'X-Powered-By': 'Vanilla' } },
    'Varnish':               {'cats': [22], 'headers': { 'X-Varnish': '.+', 'X-Varnish-Age': '.+', 'X-Varnish-Cache': '.+', 'X-Varnish-Action': '.+', 'X-Varnish-Hostname': '.+', 'Via': 'Varnish' } },
    'vBulletin':             {'cats': [2], 'meta': { 'generator': 'vBulletin' } },
    'viennaCMS':             {'cats': [1], 'html': 'powered by <a href=("|\')[^>]+viennacms' },
    'Vignette':              {'cats': [1], 'html': '<[^>]+?=("|\')(vgn\-ext|vgnext)' },
    'Vimeo':                 {'cats': [14], 'html': '<(param|embed)[^>]+vimeo\.com\/moogaloop' },
    'VirtueMart':            {'cats': [6], 'html': '<div id=("|\')vmMainPage' },
    'VisualPath':            {'cats': [10], 'script': 'visualpath[^\/]*\.trackset\.it\/[^\/]+\/track\/include\.js' },
    'Vox':                   {'cats': [11], 'url': '^(www.)?.+\.vox\.com' },
    'VP-ASP':                {'cats': [6], 'script': 'vs350\.js', 'html': '<a[^>]+>Powered By VP\-ASP Shopping Cart<\/a>' },
    'W3Counter':             {'cats': [10], 'script': 'w3counter\.com\/tracker\.js' },
    'Web Optimizer':         {'cats': [10], 'html': '<title [^>]*lang=("|\')wo("|\')>' },
    'webEdition':            {'cats': [1], 'meta': { 'generator': 'webEdition', 'DC.title': 'webEdition' } },
    'WebGUI':                {'cats': [1], 'meta': { 'generator': 'WebGUI' } },
    'WebPublisher':          {'cats': [1], 'meta': { 'generator': 'WEB\|Publisher' } },
    'WebsiteBaker':          {'cats': [1], 'meta': { 'generator': 'WebsiteBaker' } },
    'Webtrekk':              {'cats': [10], 'html': 'var webtrekk = new Object' },
    'Webtrends':             {'cats': [10], 'html': '<img[^>]+id=("|\')DCSIMG("|\')[^>]+webtrends', 'env': 'WTOptimize' },
    'Weebly':                {'cats': [1], 'html': '<[^>]+class=("|\')weebly' },
    'WikkaWiki':             {'cats': [8], 'meta': { 'generator': 'WikkaWiki' }, 'html': 'Powered by <a href=("|\')[^>]+WikkaWiki' },
    'wink':                  {'cats': [26, 12], 'script': '(\_base\/js\/base|wink).*\.js', 'env': '^wink$' },
    'Wolf CMS':              {'cats': [1], 'html': '<a href=("|\')[^>]+wolfcms.org.+Wolf CMS.+inside' },
    'Woopra':                {'cats': [10], 'script': 'static\.woopra\.com' },
    'WordPress':             {'cats': [1, 11], 'meta': { 'generator': 'WordPress' }, 'html': '<link rel=("|\')stylesheet("|\') [^>]+wp-content' },
    'xajax':                 {'cats': [12], 'script': 'xajax_core.*\.js' },
    'XenForo':               {'cats': [2], 'html': '(jQuery\.extend\(true, XenForo|Forum software by XenForo&trade;|<!\-\-XF:branding)' },
    'XiTi':                  {'cats': [10], 'html': '<[^>]+src=("|\')[^>]+xiti.com\/hit.xiti' },
    'XMB':                   {'cats': [2], 'html': '<!-- Powered by XMB' },
    'XUI':                   {'cats': [26, 12], 'script': '[^a-zA-Z]xui.*\.js', 'env': '^x\$$' },
    'XOOPS':                 {'cats': [1], 'meta': { 'generator': 'XOOPS' } },
    'xtCommerce':            {'cats': [6], 'meta': { 'generator': 'xt:Commerce' }, 'html': '<div class=("|\')copyright("|\')>.+<a[^>]+>xt:Commerce' },
    'YaBB':                  {'cats': [2], 'html': 'Powered by <a href=("|\')[^>]+yabbforum' },
    'Yahoo! Web Analytics':  {'cats': [10], 'script': 'd\.yimg\.com\/mi\/ywa\.js' },
    'Yandex.Metrika':        {'cats': [10], 'script': 'mc\.yandex\.ru\/metrika\/watch\.js' },
    'YouTube':               {'cats': [14], 'html': '<(param|embed)[^>]+youtube\.com\/v' },
    'YUI Doc':               {'cats': [4], 'html': '<html[^>]* yuilibrary\.com\/rdf\/[0-9.]+\/yui\.rdf' },
    'YUI':                   {'cats': [12], 'script': '\/yui\/|yui\.yahooapis\.com', 'env': '^YAHOO$' },
    'Zen Cart':              {'cats': [6], 'meta': { 'generator': 'Zen Cart' } },
    'Zend':                  {'cats': [18], 'headers': { 'X-Powered-By': 'Zend' } }
}



if __name__ == '__main__':
    urls = sys.argv[1:]
    if urls:
        for url in urls:
            results = reverse_engineer(url)
            for result in sorted(results.items()):
                print '%s: %s' % result
    else:
        print 'Usage: %s url1 [url2 url3 ...]' % sys.argv[0]
