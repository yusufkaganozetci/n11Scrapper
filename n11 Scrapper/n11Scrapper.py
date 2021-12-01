import requests
from bs4 import BeautifulSoup

# main program's function

def getCategoryFromDict(desiredIndex):
    desiredKey = ""
    for key, value in categoriesHolder.items():
        if value == desiredIndex:
            desiredKey = key
            break
    return desiredKey

# Functions for getAndWriteData()

def getCurrentDestination(currentPage):
    if currentPage == 1:
        return targetDestination
    else:
        return targetDestination + "?pg=" + str(currentPage + 1)

def getProductBrand(ProductFullName):
    spaceFoundIndex = 0
    for i in ProductFullName:
        if i == ' ':
            break
        else:
            spaceFoundIndex += 1
    return ProductFullName[0:spaceFoundIndex]

def getProductFullName(data):
    return data.div.div.a.h3.text.strip()

def getProductPrice(data):
    priceText = convertPriceTextToFloat(data.find("div", {"class": "proDetail"}).find("span", {"class", "newPrice cPoint priceEventClick"}).ins.text.strip(" TL\n"))
    return priceText

def convertPriceTextToFloat(ProductPriceText):
    priceText = ""
    for i in ProductPriceText:
        if i != '.':
            priceText += i
    priceText = priceText.replace(',', '.')
    return priceText

def getRating(data):
    ProductRatingText = data.span.get("class")[1]
    return ProductRatingText[1:]

def getRatingCount(data):
    ProductRatingCountText = data.find("span", {"class": "ratingText"}).text
    realPart = ProductRatingCountText[1:len(ProductRatingCountText) - 1]
    realPart = realPart.replace('.', '')
    return realPart

def getProductDealer(data):
    return data.find("span", {"class": "sallerName"}).text.strip(" \n")

def getDealerRating(data):
    return data.find("span", {"class": "point"}).text.strip(" \n")[1:]

# getAndWriteData Function

def getAndWriteData(pageCount):
    currentPage = 1
    isFirstDataPrinted=False
    while pageCount >= currentPage:
        try:
            print("page ", currentPage, "'s data has started to be sent!")
            currentLink = getCurrentDestination(currentPage)
            htmlContent = requests.get(currentLink).content
            soup = BeautifulSoup(htmlContent, "html.parser")
            if soup.find("div", {"class": "listView"}) is not None:
                listOfFoundData = soup.find("div", {"class": "listView"}).ul.find_all("li", {"class": "column"})
            else:
                listOfFoundData = soup.find("section",
                                            {"class": "group listingGroup resultListGroup import-search-view"}).find(
                    "div", {"class": "catalogView"}).ul.find_all("li", {"class": "column"})
            separator = '|'
            for data in listOfFoundData:

                ratingCont = data.find("div", {"class": "ratingCont"})
                if ratingCont is not None:
                    try:
                        productFullName = getProductFullName(data)
                        productBrand = getProductBrand(productFullName)
                        productPrice = getProductPrice(data)
                        productRating = getRating(ratingCont)
                        productRatingCount = getRatingCount(ratingCont)
                        productDealer = getProductDealer(data)
                        dealerRating = getDealerRating(data)
                        textData = productBrand + separator + productFullName + separator + productPrice + separator + productRating + separator + productRatingCount + separator + productDealer + separator + dealerRating
                        if isFirstDataPrinted:
                            dataFile.write("\n"+textData)
                        else:
                            dataFile.write(textData)
                            isFirstDataPrinted=True
                    except Exception as exc:
                        print(exc)
                        pass
            print("page ", currentPage, "'s data has successfully arrived!")
            currentPage += 1
        except Exception as e:
            print(e)
            print("n11 Scrapping is finished with errors!")
            break
    print("End of program!")

# Main Program

homePageLink = "https://www.n11.com"
dataFile = open("data.txt", "w", encoding="utf-8")
dataFile.write("ProductBrand|ProductFullName|ProductPrice|ProductRating|ProductRatingCount|ProductDealer|DealerRating" + "\n")
categoriesHolder = {"bilgisayar": 0, "saat": 1, "kitap": 2, "film": 3, "fitness-ve-kondisyon": 4,
                    "mobilya": 5, "mutfak-gerecleri": 6, "makyaj": 7, "yapi-market-ve-bahce": 8,
                    "yedek-parca-otomobil": 9}
category = ""
print("Welcome to N11 Website Scrapper!\nPlease enter a number for category or directly enter the category name!")
for key, value in categoriesHolder.items():
    print("for", key, " enter ", value)
try:
    valueFromUser = input("Please enter a category from N11:")
    category = int(valueFromUser)
    category = getCategoryFromDict(category)
except:
    category = valueFromUser
targetDestination = homePageLink + "/" + category
isWantedPageCountValid = False
wantedPageCount = 0
while not isWantedPageCountValid:
    try:
        wantedPageCount = int(input("How many pages do you want to get?(It has to be less than or equals to 50):"))
        if wantedPageCount <= 50:
            isWantedPageCountValid = True
        else:
            print("Please input a number that is less than or equals to 50!")
    except:
        print("Please input a valid number!")

getAndWriteData(wantedPageCount)