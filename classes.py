import random

timeForDelivery = 0
productsTitles = ['молоко', 'сыр', 'масло', 'колбаса', 'сгущенка', 'хлеб', 'печенье', 'шоколад', 'мармелад',
                  'гречка', 'пшено', 'макароны', 'соль', 'сахар', 'чай', 'кофе']
maxDiscount = 0.2
minDiscount = 0.01

minNecessaryCount = 100
maxNecessaryCount = 300

minCountProduct = 0
maxCountProduct = 30 # сколько розничных упаковок одного продукта может заказать магазин

minPrice = 10
maxPrice = 1000

minBeginCount = 70
maxBeginCount = 300

minShellLife = 1
maxShellLife = 10

minNumberPack = 5
maxNumberPack = 30

discountShellLife = 2

class ShopRequest:
    def __init__(self, countProducts):
        self.orderList = []
        global productsTitles
        for i in range(countProducts):
            curProduct = productsTitles[i]
            countCurProduct = random.randint(minCountProduct, maxCountProduct)
            self.orderList.append((curProduct, countCurProduct))

class WholesalePack:
    '''Оптовая упаковка'''

    def __init__(self, ProductTitle):
        self.shelfLife = random.randint(minShellLife, maxShellLife)
        self.numberPack = random.randint(minNumberPack, maxNumberPack)
        self.productTitle = ProductTitle
        self.price = random.randint(minPrice, maxPrice) # цена за розничную упаковку
        global timeForDelivery
        self.timeDelivery = timeForDelivery  # когда становится 0 - продукт получается на складе

    def makeDiscount(self, discount):
        self.price = self.price * (1 - discount)

    def getWholesalePrice(self):
        return self.numberPack * self.price

class ProviderRequest:
    def __init__(self, productsCount):
        # productsCount - [(название продукта, количество розничных упаковок)]
        self.products = []
        for (productTitle, countProduct) in productsCount:
            curWholesalePack = WholesalePack(productTitle)
            countWholesalePack = countProduct // curWholesalePack.numberPack
            self.products.append((curWholesalePack, countWholesalePack))


# поставщик говорит, сколько в его оптовой упаковке розничных, мы просим n розничных, он дает мб чуть меньше


class Warehouse:
    def __init__(self, countProducts, countShop, fullness):
        self.allCountProducts = countProducts
        self.countShop = countShop
        self.necessaryCount = {}
        self.discount = {}
        self.products = {} # для каждого продукта - список оптовых упаковок(полученных от производителя)
        self.plannedDelivery = ProviderRequest([]) # [(описание оптовой упаковки, количество оптовых упаковок)]
        self.deleted = []
        self.shopsDeficit = []
        self.sold = []
        self.money = 0
        global productsTitles, minDiscount, maxDiscount, minNecessaryCount, maxNecessaryCount
        for i in range(self.allCountProducts):
            curProductTitle = productsTitles[i]
            self.discount[curProductTitle] = random.uniform(minDiscount, maxDiscount)
            self.necessaryCount[curProductTitle] = random.randint(minNecessaryCount, maxNecessaryCount)
            beginPack = WholesalePack(curProductTitle)
            beginPack.timeDelivery = 0 # уже доставлено
            self.products[curProductTitle] = [beginPack] # какое-то начальное количество

    def receivingProducts(self):
        for i in range(len(self.plannedDelivery.products)):
            if self.plannedDelivery.products[i][0].timeDelivery == 0:
                curTitleProduct = self.plannedDelivery.products[i][0].productTitle
                for j in range(self.plannedDelivery.products[i][1]):
                    self.products[curTitleProduct].append(self.plannedDelivery.products[i][0])
            else:
                self.plannedDelivery.products[i][0].timeDelivery -= 1

    def deleteOverdue(self):
        '''Удаление просроченных'''
        deletedThisDay = []
        for productTitle in self.products.keys():
            curProducts = self.products[productTitle]
            for i in range(len(curProducts) - 1, -1, -1):
                # удаляем с конца, так что индексы ни на что не влияют
                if curProducts[i].shelfLife == 1:
                    deletedThisDay.append(curProducts[i])
                    curProducts.pop(i)
                elif curProducts[i].shelfLife == discountShellLife:
                    curProducts[i].makeDiscount(self.discount[curProducts[i].productTitle])
                else:
                    curProducts[i].shelfLife -= 1
        self.deleted.append(deletedThisDay)

    def workShopsRequests(self, allShopsRequests):
        curDaySold = []
        for curShopRequest in allShopsRequests:
            for (curProductTitle, curCount) in curShopRequest.orderList:
                beginCurCount = curCount
                curProductsList = self.products[curProductTitle]
                i = 0
                # общая стратегия - видим оптовую упаковку, меньшую, чем требуют, отдаем ее и идем искать дальше
                while i < len(curProductsList):
                    while i < len(curProductsList) and curProductsList[i].numberPack >= curCount:
                        i += 1
                    if i == len(curProductsList):
                        break                     #даем меньше, чем просят. Больше ничего дать не можем
                    curDaySold.append(curProductsList[i])
                    self.money += curProductsList[i].getWholesalePrice()
                    curCount -= curProductsList[i].numberPack
                    curProductsList.pop(i) # i - первый нерассмотренный
                if beginCurCount != 0:
                    self.shopsDeficit.append(curCount / beginCurCount) # сколько недодали
        self.sold.append(curDaySold)

    def supplierRequest(self):
        neccesaryList = []
        for curProductTitle in self.products.keys():
            countCurProduct = 0
            for curPack in self.products[curProductTitle]:
                countCurProduct += curPack.numberPack
            if countCurProduct < self.necessaryCount[curProductTitle]:
                neccesaryList.append((curProductTitle, self.necessaryCount[curProductTitle] - countCurProduct))
        self.plannedDelivery = ProviderRequest(neccesaryList)


    def newDay(self, allShopsRequests):
        self.deleteOverdue()
        self.receivingProducts()
        self.workShopsRequests(allShopsRequests)
        self.supplierRequest()

    def getInfo(self):
        global productsTitles
        return (self.money, self.deleted, self.sold, productsTitles[:self.allCountProducts])
       # return self.money

class Model:
    def __init__(self, countProducts, countShop, fullness = 0):
        self.countProducts = countProducts
        self.countShop = countShop
        self.fullness = fullness
        self.warehouse = Warehouse(countProducts, countShop, fullness)

    def nextDay(self):
        allShopsRequests = []
        for i in range(self.countShop):
            newShopRequest = ShopRequest(self.countProducts)
            allShopsRequests.append(newShopRequest)
        self.warehouse.newDay(allShopsRequests)
        return self

    def getInfo(self):
        return self.warehouse.getInfo()


m = Model(3,1,0.5)
m.nextDay()