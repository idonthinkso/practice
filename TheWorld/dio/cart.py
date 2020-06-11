from dio.models import TBookDetails


class Cart:
    def __init__(self):
        # 购物车里的商品
        self.car_items = []
        # 总计（不算运费）
        self.total_price = 0
        # 已节省的钱
        self.save_price = 0

    # 向购物车中添加商品
    def add_item(self, id, num=1):
        for item in self.car_items:
            if item.book.id == id:
                item.num += num
                # 更新购物车中的total_price和save_price
                self.calculator()
                return True
        # 如果购物车中没有该商品，则创建购物车商品对象
        book = TBookDetails.objects.get(id=id)
        cart_item = Cart_Item(book, num)
        self.car_items.append(cart_item)
        self.calculator()
        return True

    # 删除购物车中的商品
    def del_item(self, id):
        # 首先应该先找到要删除的商品
        for i in self.car_items:
            if i.book.id == id:
                self.car_items.remove(i)
                # 删完商品，应该重新计算一下购物车中的价格
                self.calculator()
                print(self.car_items)
                return True
        return False

    # 更改购物车中的商品数量
    def modify(self, id, num):
        for i in self.car_items:
            if i.book.id == id:
                i.num = num
        self.calculator()
        return

    # 计算购物车中的total_price和save_price
    def calculator(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.car_items:
            print(i.book.discount)
            print(i.book.price)
            print(i.num)
            self.total_price += i.book.discount * i.num
            self.save_price += (i.book.price - i.book.discount)*i.num
        print(self.total_price)
        print(self.save_price)



class Cart_Item:
    def __init__(self, book, num):
        '''

        :param book: 添加的书(model对象)
        :param num: 书对应的数量
        '''
        self.book = book
        self.num = num
