from heapQueue import HeapQueue

class Order:

    def __init__(self, id: int, isMarket: bool, isBuy: bool, qty: float, price: float):
        self.id = id
        self.isMarket = isMarket
        self.isBuy = isBuy
        self.price = price
        self.qty = qty

    def __str__(self):
        return str(self.id)+"("+str(self.qty)+","+str(self.price)+")"
    
    def __repr__(self):
        return str(self)

class OrderList:

    class Node:
        def __init__(self, prev = None, next = None, val = None):
            self.prev = prev
            self.next = next
            self.val = val

    def __init__(self, price: float):
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.len = 0
        self.price = price

    def __bool__(self):
        return self.len > 0
    
    def append(self, val):
        node = self.Node(self.tail.prev,self.tail,val)
        self.tail.prev.next = node
        self.tail.prev = node
        self.len += 1
        return node

    def remove(self, node):
        if node == self.head or node == self.tail:
            return None
        node.prev.next = node.next
        node.next.prev = node.prev
        self.len -= 1
        return node.val

    def pop(self):
        return self.remove(self.head.next)
    
    def first(self):
        return self.head.next.val

    def __str__(self):
        ls = []
        cur = self.head.next
        while cur != self.tail:
            ls.append(str(cur.val))
            cur = cur.next
        return str(self.price) + ": " + " ".join(ls)

    def __repr__(self):
        return str(self)
    

class Trade:
    def __init__(self, sell_order_id: int, buy_order_id: int, price: float, qty: float):
        self.sell_order_id = sell_order_id
        self.buy_order_id = buy_order_id
        self.price = price
        self.qty = qty
    
    def __str__(self):
        return "Trade sell_order: "+str(self.sell_order_id)+" buy_order: "+str(self.buy_order_id)+" price: "+str(self.price)+" qty: "+str(self.qty)

    def __repr__(self):
        return str(self)

class OrderBook:

    def __init__(self, name: str):
        self.name = name
        self.orders = {}
        self.counter = 0
        self.orderHistory = []
        self.tradeHistory: list[Trade] = []

        self.bids = HeapQueue()
        self.asks = HeapQueue()

    def placeOrder(self, isMarket: bool, isBuy: bool, qty: float, price: float = None):
        if qty <= 0:
            return
        self.counter += 1
        order = Order(self.counter, isMarket, isBuy, qty, price)
        self.orderHistory.append(Order(self.counter, isMarket, isBuy, qty, price))
        if order.isMarket:
            self.executeMarketOrder(order)
        else:
            self.placeLimitOrder(order)

    def executeMarketOrder(self, order: Order):
        heap = self.asks if order.isBuy else self.bids
        while order.qty > 0 and heap:
            self.executeTrade(order, heap)
        if order.qty > 0:
            print("Not the entire qty satisfied for market order",order.id)

    def executeTrade(self, order, heap):
        bestAskPrice, orderList = heap.peek()
        tradeOrder = orderList.first()  # assume is not None
        tradeQty = min(order.qty, tradeOrder.qty)
        order.qty -= tradeQty
        tradeOrder.qty -= tradeQty
        if tradeOrder.qty == 0:
            self.removeOrder(tradeOrder.id)
        # trade history
        buy_order_id = order.id if order.isBuy else tradeOrder.id
        sell_order_id = order.id if not order.isBuy else tradeOrder.id
        self.tradeHistory.append(Trade(sell_order_id,buy_order_id,tradeOrder.price,tradeQty))

    def executePossibleTrades(self, order: Order):
        if order.isBuy:
            while order.qty > 0 and self.asks and order.price >= self.bestAsk():
                self.executeTrade(order, self.asks)
        else:
            while order.qty > 0 and self.bids and order.price <= self.bestBid():
                self.executeTrade(order, self.bids)

    def placeLimitOrder(self, order: Order):
        # check for transactions
        self.executePossibleTrades(order)
        # place in the books
        if order.qty == 0:
            return
        if order.isBuy:
            factor, heap = -1, self.bids
        else:
            factor, heap = 1, self.asks
        orderList = heap.get(factor * order.price)
        if orderList is None:
            orderList = OrderList(order.price)
            heap.insert(factor * order.price, orderList)
        self.orders[order.id] = orderList.append(order)

    def removeOrder(self, oid):
        if oid not in self.orders:
            return False
        node = self.orders[oid]
        del self.orders[oid]
        order = node.val
        heap = self.bids if order.isBuy else self.asks
        factor = -1 if order.isBuy else 1
        orderList = heap.get(factor * order.price)
        orderList.remove(node)
        if not orderList:
            heap.remove(factor * order.price)
        return True
    
    def bestAsk(self):
        return self.asks.peek()[0] if self.asks else None
    
    def bestBid(self):
        return -self.bids.peek()[0] if self.bids else None

    def __str__(self):
        return "\nbook: " + str(self.name) + "\norders: " + str(self.orders.keys()) + "\nbids: " + str(self.bids) + "\nasks: " + str(self.asks)