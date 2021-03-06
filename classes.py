import random

TIME_FOR_DELIVERY = 0
PRODUCTS_TITLES = ['молоко', 'сыр', 'масло', 'колбаса', 'сгущенка', 'хлеб', 'печенье', 'шоколад', 'мармелад',
                   'гречка', 'пшено', 'макароны', 'соль', 'сахар', 'чай', 'кофе']
MAX_DISCOUNT = 0.2
MIN_DISCOUNT = 0.01

MIN_NECESSARY_COUNT = 100
MAX_NECESSARY_COUNT = 300

MIN_COUNT_PRODUCT = 0
MAX_COUNT_PRODUCT = 200  # сколько розничных упаковок одного продукта может заказать магазин

MIN_PRICE = 10
MAX_PRICE = 1000

MIN_BEGIN_COUNT = 70
MAX_BEGIN_COUNT = 300

MIN_SHELL_LIFE = 1
MAX_SHELL_LIFE = 10

MIN_NUMBER_PACK = 5
MAX_NUMBER_PACK = 30

DISCOUNT_SHELL_LIFE = 2

class Info:
    def __init__(self, names, last_day_sold_price, last_day_sold_count, last_day_deleted_price,
                last_day_deleted_count, all_sold_price, all_sold_count, all_deleted_price,
                all_deleted_count, all_day_shops_requests, last_day_shops_requests, all_day_shops_given,
            last_day_shops_given, balance):
        self.names = names
        self.cur_sold_price = last_day_sold_price
        self.cur_sold_count = last_day_sold_count
        self.cur_deleted_price = last_day_deleted_price
        self.cur_deleted_count = last_day_deleted_count
        self.all_sold_price = all_sold_price
        self.all_sold_count = all_sold_count
        self.all_deleted_price = all_deleted_price
        self.all_deleted_count = all_deleted_count
        self.all_shop_requests = all_day_shops_requests
        self.last_shop_requests = last_day_shops_requests
        self.all_shop_given = all_day_shops_given
        self.last_shop_given = last_day_shops_given
        self.balance = balance

class ShopRequest:
    def __init__(self, count_products):
        self.order_list = []
        global PRODUCTS_TITLES
        for i in range(count_products):
            cur_product = PRODUCTS_TITLES[i]
            count_cur_product = random.randint(MIN_COUNT_PRODUCT, MAX_COUNT_PRODUCT)
            self.order_list.append((cur_product, count_cur_product))


class WholesalePack:
    '''Оптовая упаковка'''

    def __init__(self, product_title):
        self.shelf_life = random.randint(MIN_SHELL_LIFE, MAX_SHELL_LIFE)
        self.number_pack = random.randint(MIN_NUMBER_PACK, MAX_NUMBER_PACK)
        self.product_title = product_title
        self.price = random.randint(MIN_PRICE, MAX_PRICE)  # цена за розничную упаковку
        global TIME_FOR_DELIVERY
        self.time_delivery = TIME_FOR_DELIVERY  # когда становится 0 - продукт получается на складе

    def make_discount(self, discount):
        self.price = self.price * (1 - discount)

    def get_wholesale_price(self):
        return self.number_pack * self.price


class ProviderRequest:
    def __init__(self, products_count):
        # products_count - [(название продукта, количество розничных упаковок)]
        self.products = []
        for (product_title, count_product) in products_count:
            cur_wholesale_pack = WholesalePack(product_title)
            count_wholesale_pack = count_product // cur_wholesale_pack.number_pack
            self.products.append((cur_wholesale_pack, count_wholesale_pack))


# поставщик говорит, сколько в его оптовой упаковке розничных, мы просим n розничных, он дает мб чуть меньше

def group_by_products(cur_list, names):
    ans_price_dict = {}
    ans_count_dict = {}
    for cur_name in names:
        ans_price_dict[cur_name] = 0
        ans_count_dict[cur_name] = 0
    for cur_elem in cur_list:
        if cur_elem.product_title in ans_price_dict.keys():
            ans_price_dict[cur_elem.product_title] += cur_elem.price * cur_elem.number_pack
        else:
            ans_price_dict[cur_elem.product_title] = cur_elem.price * cur_elem.number_pack

        if cur_elem.product_title in ans_count_dict.keys():
            ans_count_dict[cur_elem.product_title] += cur_elem.number_pack
        else:
            ans_count_dict[cur_elem.product_title] = cur_elem.number_pack
    return ans_price_dict, ans_count_dict


def add_new_day(all_dict, new_dict):
    for product_title in new_dict.keys():
        if product_title in all_dict.keys():
            all_dict[product_title] += new_dict[product_title]
        else:
            all_dict[product_title] = new_dict[product_title]


class Warehouse:
    def __init__(self, count_products, count_shops):
        self.all_count_products = count_products
        self.count_shops = count_shops
        self.necessary_count = {}
        self.discount = {}
        self.products = {}  # для каждого продукта - список оптовых упаковок(полученных от производителя)
        self.planned_delivery = ProviderRequest([])  # [(описание оптовой упаковки, количество оптовых упаковок)]
        self.deleted = []
        self.all_deleted_price = {}  # словарь, название - цена убытков за все время
        self.all_deleted_count = {}  # словарь, название - количество упаковок, списанных за все время
        self.all_sold_price = {}  # словарь, название товара - выручка за все время за этот товар
        self.all_sold_count = {}  # словарь, название - количество упаковок, проданных за все время
        self.last_day_deleted_price = {}  # словарь, название - цена убытков за посл. день
        self.last_day_deleted_count = {}  # словарь, название - количество упаковок, списанных за посл. день
        self.last_day_sold_price = {}  # словарь, название товара - выручка за посл.день за этот товар
        self.last_day_sold_count = {}  # словарь, название - количество упаковок, проданных за посл.день
        self.shops_deficit = []
        self.sold = []
        global PRODUCTS_TITLES, MIN_DISCOUNT, MAX_DISCOUNT, MIN_NECESSARY_COUNT, MAX_NECESSARY_COUNT
        self.names = PRODUCTS_TITLES[:self.all_count_products]
        self.money = 0
        self.shop_requests = {}
        self.last_day_shops_requests = {}  # словарь словарей
        self.last_day_shops_given = {}
        self.all_day_shops_requests = {}
        self.all_day_shops_given = {}
        for i in range(1, self.count_shops + 1):
            self.all_day_shops_requests[i] = {}
            self.all_day_shops_given[i] = {}
            for product_title in self.names:
                self.all_day_shops_requests[i][product_title] = 0
                self.all_day_shops_given[i][product_title] = 0

        for i in range(self.all_count_products):
            cur_product_title = PRODUCTS_TITLES[i]
            self.discount[cur_product_title] = random.uniform(MIN_DISCOUNT, MAX_DISCOUNT)
            self.necessary_count[cur_product_title] = random.randint(MIN_NECESSARY_COUNT, MAX_NECESSARY_COUNT)
            begin_pack = WholesalePack(cur_product_title)
            begin_pack.time_delivery = 0  # уже доставлено
            self.products[cur_product_title] = [begin_pack]  # какое-то начальное количество

    def receiving_products(self):
        for i in range(len(self.planned_delivery.products)):
            if self.planned_delivery.products[i][0].time_delivery == 0:
                cur_title_product = self.planned_delivery.products[i][0].product_title
                for j in range(self.planned_delivery.products[i][1]):
                    self.products[cur_title_product].append(self.planned_delivery.products[i][0])
            else:
                self.planned_delivery.products[i][0].time_delivery -= 1

    def delete_overdue(self):
        '''Удаление просроченных'''
        deleted_this_day = []
        for product_title in self.products.keys():
            cur_products = self.products[product_title]
            for i in range(len(cur_products) - 1, -1, -1):
                # удаляем с конца, так что индексы ни на что не влияют
                if cur_products[i].shelf_life == 1:
                    deleted_this_day.append(cur_products[i])
                    cur_products.pop(i)
                elif cur_products[i].shelf_life == DISCOUNT_SHELL_LIFE:
                    cur_products[i].make_discount(self.discount[cur_products[i].product_title])
                else:
                    cur_products[i].shelf_life -= 1
        self.deleted.append(deleted_this_day)

    def work_shops_requests(self, all_shops_requests):
        cur_day_sold = []
        for i in range(1, self.count_shops + 1):
            self.last_day_shops_requests[i] = {}
            self.last_day_shops_given[i] = {}
            for product_title in self.names:
                self.last_day_shops_requests[i][product_title] = 0
                self.last_day_shops_given[i][product_title] = 0
        for num_shop in range(len(all_shops_requests)):
            cur_shop_request = all_shops_requests[num_shop]
            for (cur_product_title, cur_count) in cur_shop_request.order_list:
                begin_cur_count = cur_count
                cur_products_list = self.products[cur_product_title]
                i = 0
                # общая стратегия - видим оптовую упаковку, меньшую, чем требуют, отдаем ее и идем искать дальше
                while i < len(cur_products_list):
                    while i < len(cur_products_list) and cur_products_list[i].number_pack >= cur_count:
                        i += 1
                    if i == len(cur_products_list):
                        break  # даем меньше, чем просят. Больше ничего дать не можем
                    cur_day_sold.append(cur_products_list[i])
                    self.money += cur_products_list[i].get_wholesale_price()
                    cur_count -= cur_products_list[i].number_pack
                    cur_products_list.pop(i)  # i - первый нерассмотренный
                if begin_cur_count != 0:
                    self.shops_deficit.append(cur_count / begin_cur_count)  # сколько недодали
                self.last_day_shops_requests[num_shop + 1][cur_product_title] = begin_cur_count
                self.last_day_shops_given[num_shop + 1][cur_product_title] = begin_cur_count - cur_count
        self.sold.append(cur_day_sold)

    def supplier_request(self):
        neccesary_list = []
        for cur_product_title in self.products.keys():
            count_cur_product = 0
            for cur_pack in self.products[cur_product_title]:
                count_cur_product += cur_pack.number_pack
            if count_cur_product < self.necessary_count[cur_product_title]:
                neccesary_list.append((cur_product_title, self.necessary_count[cur_product_title] - count_cur_product))
        self.planned_delivery = ProviderRequest(neccesary_list)

    def create_statistics(self):
        (cur_deleted_price, cur_deleted_count) = group_by_products(self.deleted[-1], self.names)
        (cur_sold_price, cur_sold_count) = group_by_products(self.sold[-1], self.names)
        self.last_day_deleted_price = cur_deleted_price
        self.last_day_deleted_count = cur_deleted_count
        self.last_day_sold_price = cur_sold_price
        self.last_day_sold_count = cur_sold_count
        add_new_day(self.all_deleted_price, cur_deleted_price)
        add_new_day(self.all_deleted_count, cur_deleted_count)
        add_new_day(self.all_sold_price, cur_sold_price)
        add_new_day(self.all_sold_count, cur_sold_count)
        for shop_numb in range(1, self.count_shops + 1):
            for product_title in self.names:
                self.all_day_shops_requests[shop_numb][product_title] += self.last_day_shops_requests[shop_numb][
                    product_title]
                self.all_day_shops_given[shop_numb][product_title] += self.last_day_shops_given[shop_numb][
                    product_title]

    def new_day(self, all_shops_requests):
        self.delete_overdue()
        self.receiving_products()
        self.work_shops_requests(all_shops_requests)
        self.supplier_request()
        self.create_statistics()

    def create_balance(self):
        balance_dict = {}
        for name in self.products.keys():
            count = 0
            for pack in self.products[name]:
                count += pack.number_pack
            balance_dict[name] = count
        return balance_dict

    def get_info(self):
        balance = self.create_balance()
        return Info(self.names, self.last_day_sold_price, self.last_day_sold_count, self.last_day_deleted_price,
                self.last_day_deleted_count, self.all_sold_price, self.all_sold_count, self.all_deleted_price,
                self.all_deleted_count, self.all_day_shops_requests, self.last_day_shops_requests, self.all_day_shops_given,
            self.last_day_shops_given, balance)


    def get_day_money(self):
        sold = 0
        for cur_prod_price in self.last_day_sold_price.values():
            sold += cur_prod_price
        deleted = 0
        for cur_prod_price in self.last_day_deleted_price.values():
            deleted += cur_prod_price
        return sold, deleted

    def get_all_money(self):
        sold = 0
        for cur_prod_price in self.all_sold_price.values():
            sold += cur_prod_price
        deleted = 0
        for cur_prod_price in self.all_deleted_price.values():
            deleted += cur_prod_price
        return sold, deleted


class Model:
    def __init__(self, count_products, count_shops, count_days, agiotage):
        self.count_products = count_products
        self.count_shops = count_shops
        self.warehouse = Warehouse(count_products, count_shops)
        self.count_days = count_days
        self.agiotage = agiotage
        self.number_day = 0
        global MIN_COUNT_PRODUCT, MAX_COUNT_PRODUCT
        MIN_COUNT_PRODUCT = round(MIN_COUNT_PRODUCT * agiotage)
        MAX_COUNT_PRODUCT = round(MAX_COUNT_PRODUCT * agiotage)

    def next_day(self):
        all_shops_requests = []
        for i in range(self.count_shops):
            new_shop_request = ShopRequest(self.count_products)
            all_shops_requests.append(new_shop_request)
        self.warehouse.new_day(all_shops_requests)
        self.number_day += 1
        return self

    def is_end(self):
        return self.number_day >= self.count_days

    def get_day_number(self):
        return self.number_day

    def get_rest_count_days(self):
        return self.count_days - self.number_day

    def get_info(self):
        return self.warehouse.get_info()

    def get_data_info(self):
        return self.count_products, self.count_shops, self.count_days, self.agiotage

    def get_count_shops(self):
        return self.count_shops

    def get_count_products(self):
        return self.count_products

    def get_day_money(self):
        return self.warehouse.get_day_money()

    def get_all_money(self):
        return self.warehouse.get_all_money()
