
# coding: utf-8

# In[1]:


from contextlib import contextmanager
import sqlite3
import os


# In[2]:


@contextmanager
def db(db_filename='stock.db'):
    
    conn = sqlite3.connect(os.path.join('..', 'data', db_filename), detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    cur = conn.cursor()
    
    yield conn, cur
    
    conn.close()


# In[3]:


def create_tables():
    
    with db() as (conn, cur):
    
        cur.execute('CREATE TABLE IF NOT EXISTS ticks (stock text, date text, open real, high real, low real, close real, adjclose real, volume integer, unique (stock, date))')
        conn.commit()
        
        cur.execute('CREATE TABLE IF NOT EXISTS headlines (stock text, date text, source text, content text UNIQUE ON CONFLICT IGNORE, rawcontent text UNIQUE ON CONFLICT IGNORE, sentimentlabel integer)')
        conn.commit()      
        
        cur.execute('CREATE TABLE IF NOT EXISTS dictionary (word text, stock text, replacement text, unique (word, stock, replacement))')
        conn.commit()


# In[4]:


def add_stock_ticks(entries):
    
    with db() as (conn, cur):
    
        cur.executemany("INSERT OR IGNORE INTO ticks VALUES (?,?,?,?,?,?,?,?)", entries)
        conn.commit()
    
def add_headlines(entries):
    
    with db() as (conn, cur):
    
        cur.executemany("INSERT OR IGNORE INTO headlines VALUES (?,?,?,?,?,?)", entries)
        conn.commit()
        
def clean_ticks():
    
    with db() as (conn, cur):
    
        cur.execute("DELETE FROM ticks WHERE adjclose='null'")
        conn.commit()


# In[5]:


def db_replace_all(query, replacement, stock='', commit=False):
    """
    Do a `replace all` on headlines in database
    
    Used to fix parsing errors of already parsed headlines
    """
    with db() as (conn, cur):
        
        cur.execute("SELECT stock, date, source, content FROM headlines WHERE stock=? AND content LIKE ?", [stock, query])
        results = cur.fetchall()
        
        for (stock, date, source, content) in results:
            
            new_content = content.replace(query.replace('%', ''), replacement)
            
            print(content)
            print(new_content)
            
            if commit:
                
                cur.execute("UPDATE headlines SET content=? WHERE stock=? AND content=?", [new_content, stock, content])
                conn.commit()
                
def do_labeling():

    with db() as (conn, cur):
        
        while True:
        
            cur.execute("SELECT content, rawcontent, sentimentlabel, stock FROM headlines ORDER BY RANDOM() LIMIT 1")
            row = cur.fetchall()[0]
            print(row)

            label = int(input())

            if label < -10:

                break
                
            else:
                
                cur.execute("UPDATE headlines SET sentimentlabel=? WHERE content=?", [label, row[0]])
                conn.commit()
        


# In[6]:


if __name__ == "__main__":
    
    create_tables()


# In[7]:


if __name__ == "__main__":
    
    ## Populate Database of Words ##
    
    hardcoded_dict = [
        ## Special Generic Tokens ##
        ["**STATISTIC**"], 
        ### Company ###
        ["**COMPANY**"], 
        ["**COMPANY**owned"],
        ["**COMPANY**s"],
        ["**COMPANY**es"],
        ["**COMPANY**stock"],
        ["ex**COMPANY**"],
        ["**COMPANY**made"],
        ["madeby**COMPANY**"],
        ["**COMPANY**com"],
        ["**COMPANY**coms"],
        ["r**COMPANY**stock"],
        ["non**COMPANY**"],
        ["**COMPANY**insider"],
        ["nasdaq**COMPANY**"],
        ["**COMPANY**cloud"],
        ["un**COMPANY**like"],
        ["**COMPANY**like"],
        ["**COMPANY**only"],
        ["**COMPANY**certified"],
        ["anti**COMPANY**"],
        ["**COMPANY**esque"],
        ["**COMPANY**ed"],
        ["**COMPANY**backed"],
        ["fbi**COMPANY**"],
        ["**COMPANY**incs"],
        ["**COMPANY**crippled"],
        ["**COMPANY**orations"],
        ["**COMPANY**oration"],
        ["**COMPANY**powered"],
        ["**COMPANY**fueled"],
        ["**COMPANY**ians"],
        ["**COMPANY**based"],
        ["**COMPANY**earnings"],
        ["**COMPANY**proof"],
        ["nasdaq**COMPANY**"],
        ["**COMPANY**news"],
        ["un**COMPANY**"],
        ["pre**COMPANY**"],
        ### Product ###
        ["**PRODUCT**phones"],
        ["**PRODUCT**com"],
        ["**PRODUCT**"],
        ["**PRODUCT**powered"],
        ["team**PRODUCT**"],
        ["**PRODUCT**like"],
        ["**PRODUCT**tablet"],
        ["**PRODUCT**authority"],
        ["ultra**PRODUCT**"],
        ["**PRODUCT**insiders"],
        ["**PRODUCT**enabled"],
        ["r**PRODUCT**s"],
        ["**PRODUCT**based"],
        ["**PRODUCT**only"],
        ["anti**PRODUCT**"],
        ["**PRODUCT**tm"],
        ["**PRODUCT**s"],
        ["non**PRODUCT**"],
        ["**PRODUCT**style"],
        ["**PRODUCT**focused"],
        ["**PRODUCT**controlled"],
        ["**PRODUCT**dev"],
        ["**PRODUCT**phone"],
        ["**PRODUCT**ly"],
        ["**PRODUCT**killer"],
        ### Member ###
        ["**MEMBER**"],
        ["**MEMBER**s"],
        ["**MEMBER**like"],
        ## Common (non-glove) Tokens ##
        ["singlecore"],
        ["nowassistant"],
        ["assistantenabled"],
        ["deeplearning"],
        ["wannacry"],
        ["wannacrypt"],
        ["qualcomms"],
        ["smartglasses"],
        ["selfdriving"],
        ["pichai"],
        ["zuckerberg"],
        ["geekwire"],
        ["uscanada"],
        ["outofstock"],
        ["outofsale"],
        ["demonetizing"],
        ["hydrogenpowered"],
        ["homebutton"],
        ["electriccar"],
        ["xamarin"],
        ["wellcalibrated"],
        ["antitrump"],
        ["multigpu"],
        ["voicerecognition"],
        ["firstgen"],
        ["secondgeneration"],
        ["thirdgeneration"],
        ["investbuy"],
        ["nearzero"],
        ["techsavvy"],
        ["steamvr"],
        ["mostlycomplete"],
        ["anticlimate"],
        ["taxbonuses"],
        ["steamos"],
        ["specialedition"],
        ["testdriving"],
        ["oneplus"],
        ["airpods"],
        ["lyft"],
        ["stockbased"],
        ["multiadapter"],
        ["tvstick"],
        ["militarygrade"],
        ["kotlin"],
        ["stockindex"],
        ["marketmoving"],
        ["belkins"],
        ["subscriptionbased"],
        ["airpod"],
        ["chiprelated"],
        ["cheapbudget"],
        ["scaledup"],
        ["wirecutter"],
        ["wristworn"],
        ["biggerscreen"],
        ["employeeranking"],
        ["stockportfolio"],
        ["firetv"],
        ["floppydisk"],
        ["zerocommission"],
        ["zenwatch"],
        ["nsagov"],
        ["fbis"],
        ["smartpost"],
        ["conflictfree"],
        ["closedsource"],
        ["communityrun"],
        ["voiceactivated"],
        ["voiceordered"],
        ["safetynet"],
        ["gsync"],
        ["chromecast"],
        ["jpmorgans"],
        ["septupled"],
        ["liquidresistant"],
        ["brexit"],
        ["meltdownspectre"],
        ["multiwaypoint"],
        ["carplay"],
        ["hotword"],
        ["nearstock"],
        ["mindblank"],
        ["thermalpower"],
        ["datascience"],
        ["spotifys"],
        ["bigheavy"],
        ["stockpicks"],
        ["mediastore"],
        ["forceclosed"],
        ["trudeaus"],
        ["upgradekits"],
        ["autoorientation"],
        ["ryzen"],
        ["computershared"],
        ["hypetrain"],
        ["adaptercharger"],
        ["bigbasket"],
        ["muslimban"],
        ["samsungbuilt"],
        ["unesthetic"],
        ["outlookcom"],
        ["postsnowden"],
        ["hashrate"],
        ["yoloed"],
        ["halfsalary"],
        ["neweggcom"],
        ["newegg"],
        ["hyperlapse"],
        ["snapchats"],
        ["browserhijacking"],
        ["iconpack"],
        ["vpnbased"],
        ["onecore"],
        ["russianlinked"],
        ["playerunknowns"],
        ["russianbought"],
        ["instacart"],
        ["intelbacked"],
        ["pointzero"],
        ["snapchatlike"],
        ["housesharing"],
        ["waymo"],
        ["bugglitch"],
        ["xiaomi"],
        ["driverlesscar"],
        ["selfdrivingcar"],
        ["axpowered"],
        ["intelliglass"],
        ["aiinfused"],
        ["hathawaylike"],
        ["airdelivery"],
        ["trumpian"],
        ["higheragain"],
        ["batterieskeep"],
        ["topreferrer"],
        ["litecoin"],
        ["gearvr"],
        ["lightsail"],
        ["autovoice"],
        ["dnapowered"],
        ["profitsurging"],
        ["ballooninternet"],
        ["amazonvisa"],
        ["antiencryption"],
        ["undisruptive"],
        ["lumentum"],
        ["renderingtext"],
        ["expectationcrushing"],
        ["microbezel"],
        ["bezelless"],
        ["cryptocurrencies"],
        ["softcard"],
        ["millionairemaker"],
        ["debtpowered"],
        ["nonxl"],
        ["panoramafunction"],
        ["applesized"],
        ["quartercrushing"],
        ["internetofthings"],
        ["marginexpansion"],
        ["linkedins"],
        ["phoneshaped"],
        ["chipgate"],
        ["userbench"],
        ["webwrapper"],
        ["marketfoolery"],
        ["salesforcecom"],
        ["cybershopping"],
        ["hewlettpackards"],
        ["nratv"],
        ["portraitmode"],
        ["unitedhealths"],
        ["vivebrand"],
        ["dtouch"],
        ["nvidia"],
        ["evga"],
        ["csipa"],
        ["wsj"],
        ["spectre"],
        ["mobileyes"],
        ["mobileye"],
        ["oracle"],
        ["hynix"],
        ["openbsds"],
        ["corecount"],
        ["lowestvolume"],
        ["crashiversary"],
        ["adaptivesync"],
        ["aifocused"],
        ["recordbound"],
        ["eighthgen"],
        ["serverchip"],
        ["baseclock"],
        ["dollarstock"],
        ["allcore"],
        ["nasdaqs"],
        ["dividendgrowers"],
        ["aramco"],
        ["wsj"],
        ["nm"],
        ["globalfoundries"],
        ["applemusic"],
        ["ipodbased"],
        ["stockpure"],
        ["accentures"],
        ["latestacquisition"],
        ["microcenters"],
        ["nokita"],
        ["customstock"],
        ["finfet"],
        ["highestconviction"],
        ["madebygoogle"],
        ["stockarriving"],
        ["nolongerupdated"],
        ["truedepth"],
        ["phonecases"],
        ["chromecasts"],
        ["nraboycott"],
        ["unibail"],
        ["profitkilling"],
        ["touchbar"],
        ["releveraging"],
        ["iwatches"],
        ["lumentums"],
        ["costpertransistor"],
        ["zenphones"],
        ["highertiered"],
        ["zenbased"],
        ["stressrun"],
        ["pcieslot"],
        ["autonomousdriving"],
        ["dowdriving"],
        ["cashhoarding"],
        ["stockafter"],
        ["hololens"],
        ["shiftlow"],
        ["sneakygood"],
        ["rxadvance"],
        ["ceoinchief"],
        ["belpointe"],
        ["realitypowered"],
        ["postspectre"],
        ["autosignature"],
        ["adpolicy"],
        ["mostsatisfied"],
        ["cloudonly"],
        ["lowmultiple"],
        ["huffingtons"],
        ["arpowered"],
        ["stockgrant"],
        ["millionpeople"],
        ["earningsdriven"],
        ["onceprohibited"],
        ["cloudheavy"],
        ["networkcloud"],
        ["nramembers"],
        ["agtech"],
        ["batterygate"],
        ["allegion"],
        ["hardwareasaservice"],
        ["gpedevices"],
        ["irisscanning"],
        ["graphicschip"],
        ["amazoncoms"],
        ["scaringoff"],
        ["edgesqueeze"],
        ["digitalassistant"],
        ["vehiclebuying"],
        ["intelligenceenabled"],
        ["mostrevolutionary"],
        ["cameramaker"],
        ["citigroups"],
        ["thesischanging"],
        ["trumpbubble"],
        ["coinbase"],
        ["xively"],
        ["alibabalinked"],
        ["cityman"],
        ["marketsfocused"],
        ["familyfriends"],
        ["ryzenoptimized"],
        ["betterthanfeared"],
        ["volocopter"],
        ["lyfts"],
        ["smalltablet"],
        ["energous"],
        ["billrelated"],
        ["siripowered"],
        ["connectedcar"],
        ["zillows"],
        ["posttrump"],
        ["earningsfilled"],
        ["weakdollar"],
        ["dropboxs"],
        ["chinesebrand"],
        ["inrelease"],
        ["schlumbergers"],
        ["morningarrests"],
        ["bombedinstantly"],
        ["exnokia"],
        ["hundredpoint"],
        ["ridehailing"],
        ["bitcoinrelated"],
        ["unceo"],
        ["cashierless"],
        ["vmwares"],
        ["internationalflavored"],
        ["bioverativ"],
        ["gigafactory"],
        ["curvedscreen"],
        ["hurricanerecovery"],
        ["pipowered"],
        ["applekilling"],
        ["biasedgoggles"],
        ["postbrexit"],
        ["samsungesque"],
        ["geekstock"],
        ["alibabas"],
        ["voat"],
        ["buyrated"],
        ["miniflash"],
        ["artificialintelligencerelated"],
        ["nanoshuffle"],
        ["viacoms"],
        ["celegene"],
        ["bigdividend"],
        ["aipowered"],
        ["wsjs"],
        ["phonetracking"],
        ["waymos"],
        ["cloudfocused"],
        ["cryptocurrencys"],
        ["instacarts"],
        ["multistock"],
        ["withbuyout"],
        ["softbanks"],
        ["smallercap"],
        ["indexbuying"],
        ["lowtaxed"],
        ["obieaward"],
        ["forbescom"],
        ["equifaxed"],
        ["datafree"],
        ["asialisted"],
        ["billionaireapproved"],
        ["donglegate"],
        ["bigvolume"],
        ["privatelink"],
        ["siliconlottery"],
        ["aggressivelypriced"],
        ["instantwatcher"],
        ["exgoogle"],
        ["exfacebook"],
        ["cloudyn"],
        ["sandp"],
        ["bezelfree"],
        ["sandisks"],
        ["yetunproven"],
        ["nonrgb"],
        ["smartdoorbell"],
        ["airdisplay"],
        ["echokiller"],
        ["ambientsense"],
        ["secondquarters"],
        ["satellitelaunching"],
        ["terrorisminspired"],
        ["semiconductormakers"],
        ["cloudfirst"],
        ["internetorg"],
        ["moffettnathanson"],
        ["salesforcecoms"],
        ["cashierfree"],
        ["covfefe"],
        ["norush"],
        ["longdominated"],
        ["exhedge"],
        ["highvaluation"],
        ["chipdesign"],
        ["ryzens"],
        ["hotperforming"],
        ["miningequipment"],
        ["pathtraced"],
        ["firefoxs"],
        ["linuxs"],
        ["dowduponts"],
        ["facebookesque"],
        ["airelated"],
        ["bottomfiring"],
        ["riskreversal"],
        ["valueacts"],
        ["minisilicon"],
        ["biogens"],
        ["chemchina"],
        ["mckessons"],
        ## Specialized Tokens ##
        ### MSFT ###
        ["onedrive", "MSFT", "**PRODUCT**"],
        ["bing", "MSFT", "**PRODUCT**"],
        ["xbox one x", "MSFT", "**PRODUCT**"],
        ["satya nadella", "MSFT", "**MEMBER**"],
        ["satyanadella", "MSFT", "**MEMBER**"],
        ["nadella", "MSFT", "**MEMBER**"],
        ["steve ballmer", "MSFT", "**MEMBER**"],
        ["bill gates", "MSFT", "**MEMBER**"],
        ["microsoft", "MSFT", "**COMPANY**"],
        ["microsoft corporation", "MSFT", "**COMPANY**"],
        ["microsoft corp", "MSFT", "**COMPANY**"],
        ["microsoft corporate", "MSFT", "**COMPANY**"],
        ["msft", "MSFT", "**COMPANY**"],
        ["outlook", "MSFT", "**PRODUCT**"],
        ["hololens", "MSFT", "**PRODUCT**"],
        ["xbox one", "MSFT", "**PRODUCT**"],
        ["windows", "MSFT", "**PRODUCT**"],
        ["windowsoffice", "MSFT", "**PRODUCT**"],
        ["xbox", "MSFT", "**PRODUCT**"],
        ### AMD ###
        ["radeon rxvega", "AMD", "**PRODUCT**"],
        ["rxvega", "AMD", "**PRODUCT**"],
        ["advanced micro devices", "AMD", "**COMPANY**"],
        ["radeon vega frontier edition", "AMD", "**PRODUCT**"],
        ["lisa su", "AMD", "**MEMBER**"],
        ["lisasu", "AMD", "**MEMBER**"],
        ["woligrowski", "AMD", "**MEMBER**"],
        ["radeon", "AMD", "**PRODUCT**"],
        ["zen", "AMD", "**PRODUCT**"],
        ["amd", "AMD", "**COMPANY**"],
        ["vega fe", "AMD", "**PRODUCT**"],
        ["ryzen", "AMD", "**PRODUCT**"],
        ["r fury", "AMD", "**PRODUCT**"],
        ["radeon fury", "AMD", "**PRODUCT**"],
        ### AMZN ###
        ["echo", "AMZN", "**PRODUCT**"],
        ["alexa", "AMZN", "**PRODUCT**"],
        ["prime video", "AMZN", "**PRODUCT**"],
        ["firephone", "AMZN", "**PRODUCT**"],
        ["amazon", "AMZN", "**COMPANY**"],
        ["amzn", "AMZN", "**COMPANY**"],
        ["jeff bezos", "AMZN", "**MEMBER**"],
        ["amazondot", "AMZN", "**PRODUCT**"],
        ["firetv", "AMZN", "**PRODUCT**"],
        ["jeffbezos", "AMZN", "**MEMBER**"],
        ["fire tv", "AMZN", "**PRODUCT**"],
        ["fire tv stick", "AMZN", "**PRODUCT**"],
        ["amazonfire", "AMZN", "**PRODUCT**"],
        ["amazonfresh", "AMZN", "**PRODUCT**"],
        ["primeday", "AMZN", "**PRODUCT**"],
        ["dot", "AMZN", "**PRODUCT**"],
        ["amazonvisa", "AMZN", "**PRODUCT**"],
        ["prime", "AMZN", "**PRODUCT**"],
        [" dash", "AMZN", " **PRODUCT**"],
        ["smileamazoncom", "AMZN", "**PRODUCT**"],
        ["amazonsmile", "AMZN", "**PRODUCT**"],
        ["deeplens", "AMZN", "**PRODUCT**"],
        ### AAPL ###
        ["lightningpin", "AAPL", "**PRODUCT**"],
        ["siri", "AAPL", "**PRODUCT**"],
        ["iphone", "AAPL", "**PRODUCT**"],
        ["iphone x", "AAPL", "**PRODUCT**"],
        ["applepark", "AAPL", "**PRODUCT**"],
        ["iphonex", "AAPL", "**PRODUCT**"],
        ["airpods", "AAPL", "**PRODUCT**"],
        ["macbook", "AAPL", "**PRODUCT**"],
        ["appletv", "AAPL", "**PRODUCT**"],
        ["applepay", "AAPL", "**PRODUCT**"],
        ["apple", "AAPL", "**COMPANY**"],
        ["aapl", "AAPL", "**COMPANY**"],
        ["imessage", "AAPL", "**PRODUCT**"],
        ["iwatch", "AAPL", "**PRODUCT**"],
        ["macbook air", "AAPL", "**PRODUCT**"],
        ["mac ", "AAPL", "**PRODUCT** "],
        ["icloud", "AAPL", "**PRODUCT**"],
        ["applewatch", "AAPL", "**PRODUCT**"],
        ["facetime", "AAPL", "**PRODUCT**"],
        ["animoji", "AAPL", "**PRODUCT**"],
        ["faceid", "AAPL", "**PRODUCT**"],
        ["face id", "AAPL", "**PRODUCT**"],
        ["imac", "AAPL", "**PRODUCT**"],
        ["ios", "AAPL", "**PRODUCT**"],
        [" d touch", "AAPL", " **PRODUCT**"],
        [" dtouch", "AAPL", " **PRODUCT**"],
        ["ipad", "AAPL", "**PRODUCT**"],
        ["touchid", "AAPL", "**PRODUCT**"],
        ["tim cook", "AAPL", "**MEMBER**"],
        ["timcook", "AAPL", "**MEMBER**"],
        ["applemusic", "AAPL", "**PRODUCT**"],
        ["homekit", "AAPL", "**PRODUCT**"],
        ["homepod", "AAPL", "**PRODUCT**"],
        ### GOOG ###
        ["nexusx", "GOOG", "**PRODUCT**"],
        ["pixel xl", "GOOG", "**PRODUCT**"],
        ["pixelxl", "GOOG", "**PRODUCT**"],
        ["pixel", "GOOG", "**PRODUCT**"],
        ["chrome", "GOOG", "**PRODUCT**"],
        ["googlephotos", "GOOG", "**PRODUCT**"],
        ["chromecast", "GOOG", "**PRODUCT**"],
        ["chromebook", "GOOG", "**PRODUCT**"],
        ["googleplay", "GOOG", "**PRODUCT**"],
        ["android", "GOOG", "**PRODUCT**"],
        ["nexusp", "GOOG", "**PRODUCT**"],
        ["nexus", "GOOG", "**PRODUCT**"],
        ["maps", "GOOG", "**PRODUCT**"],
        [" allo ", "GOOG", " **PRODUCT** "],
        ["youtube", "GOOG", "**PRODUCT**"],
        ["googletranslate", "GOOG", "**PRODUCT**"],
        ["alphabet", "GOOG", "**COMPANY**"],
        ["goog", "GOOG", "**COMPANY**"],
        ["googlealphabet", "GOOG", "**COMPANY**"],
        ["androidpay", "GOOG", "**PRODUCT**"],
        ["googlehome", "GOOG", "**PRODUCT**"],
        ["google fiber", "GOOG", "**PRODUCT**"],
        ["play store", "GOOG", "**PRODUCT**"],
        ["googlemusic", "GOOG", "**PRODUCT**"],
        ["sundar pichai", "GOOG", "**MEMBER**"],
        ["gboard", "GOOG", "**PRODUCT**"],
        ["alphago", "GOOG", "**PRODUCT**"],
        ["sundarpichai", "GOOG", "**MEMBER**"],
        ["materialdesign", "GOOG", "**PRODUCT**"],
        ["google", "GOOG", "**COMPANY**"],
        ["waymos", "GOOG", "**COMPANY**"],
        ### INTC ###
        ["intel", "INTC", "**COMPANY**"],
        ["core i cpu", "INTC", "**PRODUCT**"],
        ["coffee lake", "INTC", "**PRODUCT**"],
        ["coffeelake", "INTC", "**PRODUCT**"],
        ["icelake", "INTC", "**PRODUCT**"],
        ["ice lake", "INTC", "**PRODUCT**"],
        ["kaby lake", "INTC", "**PRODUCT**"],
        ["thgen cpu", "INTC", "**PRODUCT**"],
        [" thgen ", "INTC", " **PRODUCT** "],
        ["corei", "INTC", "**PRODUCT**"],
        ["intel cpu", "INTC", "**PRODUCT**"],
        ["i cpu", "INTC", "**PRODUCT**"],
        [" i ", "INTC", " **PRODUCT** "],
        ["igpus", "INTC", "**PRODUCT**"],
        [" thgeneration", "INTC", " **PRODUCT**"],
        ["zeon", "INTC", "**PRODUCT**"],
        ["zeon phi", "INTC", "**PRODUCT**"],
        ["xseries", "INTC", "**PRODUCT**"],
        ["core i xe", "INTC", "**PRODUCT**"],
        ["sandy bridge", "INTC", "**PRODUCT**"],
        ["skylake", "INTC", "**PRODUCT**"],
        ["haswell", "INTC", "**PRODUCT**"],
        ["brain krzabnich", "INTC", "**MEMBER**"],
        ["otellini", "INTC", "**MEMBER**"],
        ["paul otellini", "INTC", "**MEMBER**"],
        ["krzabnich", "INTC", "**MEMBER**"],
        ["kabylake", "INTC", "**PRODUCT**"],
        ["realsense", "INTC", "**PRODUCT**"],
        ["movidius", "INTC", "**PRODUCT**"],
        ["omnipath", "INTC", "**PRODUCT**"],
        ["intc", "INTC", "**COMPANY**"]
    ]
    
    for item in hardcoded_dict:
        
        if len(item) == 1:
            item.extend(['none', item[0]])
    
    with db() as (conn, cur):
    
        cur.executemany("INSERT OR IGNORE INTO dictionary VALUES (?,?,?)", hardcoded_dict)
        conn.commit()
    

