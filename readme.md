# Order Book Implementation
A high-performance order matching engine implemented in Python, featuring a **custom heap**.

## Features
- **Limit Orders**: Place orders at specific price levels
- **Market Orders**: Execute immediately at best available prices
- **Order Cancellation**: Remove orders from the book in O(1) time
- **Price-Time Priority**: FIFO matching at each price level
- **Automatic Matching**: Real-time order matching engine
- **Trade History**: Complete record of all executed trades

## Architecture

### Core Components

#### 1. **Custom Heap (`HeapQueue`)**
A binary min-heap built from scratch to support **O(log n) arbitrary deletion** — something Python's built-in `heapq` does not support.

```
HeapQueue
├── Array-based binary tree
├── insert(key, val)    → O(log n), 
├── pop()               → O(log n), removes minimum and returns key and value
├── remove(key)         → O(log n), removes any value with this key directly
└── peek()              → O(1)
```

Key design: Keeping a hash map with the existing key values and their position in the array tree.

#### 2. **Dual Heap Structure**
```
bids: HeapQueue
   └── {-price: OrderList}
         └── Node → Node → Node (doubly-linked)
               ↓      ↓      ↓
             Order  Order  Order
 asks: HeapQueue
   └── {price: OrderList}
         └── Node → Node → Node (doubly-linked)
               ↓      ↓      ↓
             Order  Order  Order
```

#### 3. **OrderList (Doubly-Linked List)**
Each price level holds a doubly-linked list of orders for strict FIFO ordering:

- O(1) insertion 
- O(1) removal 
- Guarantees time priority within a price level

#### 4. **Hash Map for O(1) Lookups**
```python
orders:  order_id → ListNode   # O(1) access to list node
```

### Full Architecture
```
OrderBook
├── bids/asks: HeapQueue
├── orders: {order_id: Node}  ← Direct node reference
└── data
      ├── record of all orders
      └── record of all executed trades
```

### Data Flow
```
New Order Arrives
   ↓
Check for Immediate Matches
   ↓
If Match Found → Execute Trade
   ├── Update quantities
   ├── Remove filled orders from OrderList  O(1)
   ├── If price level empty → heap.remove(price)  O(log n)
   └── Record trade
   ↓
If Quantity Remains → Add to Book
   ├── Find/create price level in heap  O(1) / O(log n)
   ├── Append to OrderList (FIFO)       O(1)
   └── Store reference in hash map      O(1)
```

## Time Complexity

k = number of different price levels

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| **Add Order (new price)** | O(log k) | Heap insert |
| **Add Order (existing price)** | O(1) | List append |
| **Cancel Order** | O(1) | Dict lookup + List removal |
| **Remove Empty Price Level** | O(log k) | Direct price removal via HeapQueue |
| **Get Best Bid/Ask** | O(1) | Heap peek |
| **Execute Trade** | O(log k) | List ops + heap removal if level empties |
| **Match Orders** | O(m log k) | m = number of price levels swept |

**Space**: O(n) — n active orders, one heap node per price level

> The custom heap eliminates the need for lazy deletion. Price levels are removed **immediately** when empty, keeping the heap clean at all times.

## Files
| File | Description |
|------|-------------|
| `orderBook.py` | Order book implementation |
| `heapQueue.py` | Custom array-based heap |
| `test_order_book.py` | Test suite |
| `heapQueueTesting.py` | Test queue implementation |

## Testing
```bash
python3 test_order_book.py
```

### Test Coverage
- ✅ Basic limit order placement
- ✅ Immediate order matching
- ✅ FIFO priority verification
- ✅ Market order execution
- ✅ Partial fill handling
- ✅ Order cancellation + heap cleanup
- ✅ Price improvement
- ✅ Multiple price levels
- ✅ Empty book edge cases
- ✅ Stress testing (100+ orders)
