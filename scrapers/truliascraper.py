from bs4 import BeautifulSoup
import urllib2

home_url = "http://www.trulia.com"
    
start_links = [ 
    "http://www.trulia.com/for_rent/Santa_Clara,CA/0-1700_price/37.33893375629936,37.38914209855501,-122.13229779822069,-121.80717115027147_xy/12_zm/"
]

def getAllApartments():
    links = []
    # Gather all the links in the start links 
    for link in start_links:
        links.append(link)
        
        response = urllib2.urlopen(link)
        data = response.read()
        soup = BeautifulSoup(data)
        
        # Grab all the links in the pagination div  
        new_links = getLinks(soup)
        links.extend(new_links)

    for link in links:
        print link
        response = urllib2.urlopen(link)
        data = response.read()
        soup = BeautifulSoup(data)
   
        # Extract all the card bodies that hold the individual apartments
        cardBodies = soup.find_all("div", class_="cardBody")
        for cardBody in cardBodies:
            #cardBody = BeautifulSoup(cardBody)
            getApartment(cardBody)
            
def getApartment(cardBody):
    sA = getStreetAddress(cardBody)
    rA = getRegionAddress(cardBody)
    address = sA + ', ' + rA 
    price = getPrice(cardBody)
    desc = getDesc(cardBody)
    link = getLink(cardBody)
    bedrooms = getBedrooms(desc)
    print address
    print 'price: ' + price 
    print 'desc: ' + unicode(desc).encode('utf-8') 
    print 'link: ' + link
    print 'bd: ' + bedrooms 
    return
    #Get media body, for the title, link, description and price
   
def getLink(cardBody): 
    a = cardBody.find("a", class_="primaryLink typeTruncate pdpLink pdpLinkRental")
    return 'http://www.trulia.com' + a.attrs["href"]

def getPrice(cardBody): 
    div = cardBody.find("div", class_="col lastCol txtR")
    span = div.find("span", class_="h4")
    strong = span.find("strong")
    return strong.string

"""
The description on trulia is sometimes found in the title, and sometimes 
underneath the price. This description will combine both 
"""
def getDesc(cardBody): 
    title = cardBody.find("strong", attrs={"itemprop" : "name"}).string
    div = div = cardBody.find("div", class_="col lastCol txtR") 
    desc = div.find("p", class_="man").string
    if desc is None:
        return title.strip(' \t\n\r')
    return title.strip(' \t\n\r') + ' ' + desc.strip(' \t\n\r')
    
def getStreetAddress(cardBody):
    streetAddress = cardBody.find("span", attrs={"itemprop": "streetAddress"})
    return streetAddress.string
    
def getRegionAddress(cardBody):
    addressLocality = cardBody.find("span", attrs={"itemprop" : "addressLocality"}).string
    addressRegion = cardBody.find("span", attrs={"itemprop" : "addressRegion"}).string
    postalCode = cardBody.find("span", attrs={"itemprop" : "postalCode"}).string
    
    return addressLocality + ', ' + addressRegion + ' ' + postalCode
    
"""
From the description, determines if the apartment has "bd" or "bedroom" 
and from there extracts the number of bedrooms, returns an empty string
if nothing was found
"""
def getBedrooms(description): 
    bdPos = description.find('bd')
    bedroom = description.find('bedroom')
    if bdPos != -1:
        if bdPos >= 2: return description[bdPos-2:bdPos].replace(" ", "")
        else : return description[bdPos-1:bdPos].replace(" ", "")
    elif bedroom != -1:
        if bedroom >= 2: return description[bedroom-2:bedroom].replace(" ", "")
        else: return description[bedroom-2:bedroom].replace(" ", "")
    return ""

"""
Grabs the links from the pagination div, returned by 
"""
def getLinks(soup):
    pageDiv = soup.find("div", class_="col cols16 mts txtC srpPagination_list")
    atags = pageDiv.findAll("a")
    
    links = []
    for a in atags:
        links.append(home_url + a.attrs["href"]); 
        
    return links
        
 
    