"""
Comprehensive Test Suite for Order Book
========================================
Tests all edge cases and functionality
"""

from orderBook import OrderBook

def test_basic_limit_orders():
    """Test 1: Basic limit order placement"""
    print("=" * 60)
    print("TEST 1: Basic Limit Order Placement")
    print("=" * 60)
    
    book = OrderBook("TEST1")
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=10)
    book.placeOrder(isBuy=True, isMarket=False, price=99, qty=5)
    book.placeOrder(isBuy=False, isMarket=False, price=101, qty=8)
    book.placeOrder(isBuy=False, isMarket=False, price=102, qty=12)
    
    assert book.bestBid() == 100, f"Expected best bid 100, got {book.bestBid()}"
    assert book.bestAsk() == 101, f"Expected best ask 101, got {book.bestAsk()}"
    assert len(book.orders) == 4, f"Expected 4 orders, got {len(book.orders)}"
    assert len(book.tradeHistory) == 0, "No trades should have occurred"
    
    print("✅ PASSED: Best bid = 100, Best ask = 101, No trades")
    print()


def test_immediate_matching():
    """Test 2: Orders that match immediately"""
    print("=" * 60)
    print("TEST 2: Immediate Order Matching")
    print("=" * 60)
    
    book = OrderBook("TEST2")
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=10)
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=5)  # Should match
    
    assert len(book.tradeHistory) == 1, f"Expected 1 trade, got {len(book.tradeHistory)}"
    assert book.tradeHistory[0].qty == 5, "Trade quantity should be 5"
    assert book.tradeHistory[0].price == 100, "Trade price should be 100"
    
    # Check remaining order
    remaining_order = list(book.orders.values())[0].val
    assert remaining_order.qty == 5, f"Remaining qty should be 5, got {remaining_order.qty}"
    assert not remaining_order.isBuy, "Remaining order should be a sell"
    
    print("✅ PASSED: 5 units traded at 100, 5 units remaining")
    print()


def test_fifo_matching():
    """Test 3: Price-time priority (FIFO) at same price"""
    print("=" * 60)
    print("TEST 3: FIFO Matching (Price-Time Priority)")
    print("=" * 60)
    
    book = OrderBook("TEST3")
    # Add multiple sells at same price
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=10)  # Order 1
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=20)  # Order 2
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=15)  # Order 3
    
    # Buy order should match Order 1 first
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=25)
    
    assert len(book.tradeHistory) == 2, f"Expected 2 trades, got {len(book.tradeHistory)}"
    assert book.tradeHistory[0].sell_order_id == 1, "First trade should use order 1"
    assert book.tradeHistory[0].qty == 10, "First trade qty should be 10"
    assert book.tradeHistory[1].sell_order_id == 2, "Second trade should use order 2"
    assert book.tradeHistory[1].qty == 15, "Second trade qty should be 15"
    
    # Order 2 should have 5 remaining
    remaining_order = book.orders[2].val
    assert remaining_order.qty == 5, f"Order 2 should have 5 remaining, got {remaining_order.qty}"
    
    print("✅ PASSED: FIFO order maintained - matched orders 1, 2 in sequence")
    print()


def test_market_order_buy():
    """Test 4: Market buy order"""
    print("=" * 60)
    print("TEST 4: Market Buy Order")
    print("=" * 60)
    
    book = OrderBook("TEST4")
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=10)
    book.placeOrder(isBuy=False, isMarket=False, price=101, qty=15)
    book.placeOrder(isBuy=False, isMarket=False, price=102, qty=20)
    
    # Market buy for 30 units - should sweep multiple levels
    book.placeOrder(isBuy=True, isMarket=True, qty=30)
    
    assert len(book.tradeHistory) == 3, f"Expected 3 trades, got {len(book.tradeHistory)}"
    assert book.tradeHistory[0].price == 100, "First trade at 100"
    assert book.tradeHistory[1].price == 101, "Second trade at 101"
    assert book.tradeHistory[2].price == 102, "Third trade at 102"
    assert book.tradeHistory[2].qty == 5, "Last trade should be 5 units"
    
    # Check remaining
    assert book.bestAsk() == 102, "Best ask should be 102"
    remaining = book.orders[3].val
    assert remaining.qty == 15, f"15 units should remain at 102, got {remaining.qty}"
    
    print("✅ PASSED: Market order swept through 3 price levels")
    print()


def test_market_order_partial_fill():
    """Test 5: Market order with insufficient liquidity"""
    print("=" * 60)
    print("TEST 5: Market Order Partial Fill (Insufficient Liquidity)")
    print("=" * 60)
    
    book = OrderBook("TEST5")
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=10)
    
    # Try to buy 20 when only 10 available
    print("Expecting warning message:")
    book.placeOrder(isBuy=True, isMarket=True, qty=20)
    
    assert len(book.tradeHistory) == 1, "Should have 1 trade"
    assert book.tradeHistory[0].qty == 10, "Should trade only 10 units"
    # print(book.orders)
    assert len(book.orders) == 0, "Book should be empty"
    
    print("✅ PASSED: Partial fill with warning")
    print()


def test_order_cancellation():
    """Test 6: Order cancellation"""
    print("=" * 60)
    print("TEST 6: Order Cancellation")
    print("=" * 60)
    
    book = OrderBook("TEST6")
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=10)   # Order 1
    book.placeOrder(isBuy=True, isMarket=False, price=99, qty=5)     # Order 2
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=8)    # Order 3
    
    # Cancel order 1
    result = book.removeOrder(1)
    assert result == True, "Cancellation should succeed"
    assert 1 not in book.orders, "Order 1 should be removed"
    assert book.bestBid() == 100, "Best bid still 100 (order 3)"
    
    # Cancel order 3
    book.removeOrder(3)
    assert book.bestBid() == 99, "Best bid should now be 99"
    
    # Try to cancel non-existent order
    result = book.removeOrder(999)
    assert result == False, "Should fail for non-existent order"
    
    print("✅ PASSED: Cancellation works correctly")
    print()


def test_partial_fills():
    """Test 7: Multiple partial fills"""
    print("=" * 60)
    print("TEST 7: Multiple Partial Fills")
    print("=" * 60)
    
    book = OrderBook("TEST7")
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=50)
    
    # Multiple sells that partially fill the buy
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=10)  # Match 10
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=15)  # Match 15
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=20)  # Match 20
    
    assert len(book.tradeHistory) == 3, "Should have 3 trades"
    assert sum(t.qty for t in book.tradeHistory) == 45, "Total traded should be 45"
    
    # Original buy order should have 5 remaining
    buy_order = book.orders[1].val
    assert buy_order.qty == 5, f"Buy order should have 5 remaining, got {buy_order.qty}"
    
    print("✅ PASSED: Multiple partial fills work correctly")
    print()


def test_price_improvement():
    """Test 8: Better price execution"""
    print("=" * 60)
    print("TEST 8: Price Improvement")
    print("=" * 60)
    
    book = OrderBook("TEST8")
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=10)
    book.placeOrder(isBuy=False, isMarket=False, price=99, qty=10)
    
    # Buy at 100, should execute at 99 (better price)
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=5)
    
    assert book.tradeHistory[0].price == 99, "Should execute at better price (99)"
    assert book.bestAsk() == 99, "99 level should still have 5 units"
    
    print("✅ PASSED: Executed at better price")
    print()


def test_multiple_price_levels():
    """Test 9: Order spanning multiple price levels"""
    print("=" * 60)
    print("TEST 9: Order Spanning Multiple Price Levels")
    print("=" * 60)
    
    book = OrderBook("TEST9")
    # Build sell side
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=5)
    book.placeOrder(isBuy=False, isMarket=False, price=101, qty=10)
    book.placeOrder(isBuy=False, isMarket=False, price=102, qty=15)
    book.placeOrder(isBuy=False, isMarket=False, price=103, qty=20)
    
    # Large buy order at 102 - should sweep 100, 101, 102
    book.placeOrder(isBuy=True, isMarket=False, price=102, qty=25)
    
    assert len(book.tradeHistory) == 3, "Should trade across 3 levels"
    assert book.tradeHistory[0].price == 100, "First at 100"
    assert book.tradeHistory[1].price == 101, "Second at 101"
    assert book.tradeHistory[2].price == 102, "Third at 102"
    assert sum(t.qty for t in book.tradeHistory) == 25, "Total 25 traded"
    
    # 103 level should remain untouched
    assert book.bestAsk() == 102, "Best ask should be 102"
    assert book.orders[3].val.qty == 5, "5 units remaining at 102"
    
    print("✅ PASSED: Correctly swept through multiple price levels")
    print()


def test_empty_book():
    """Test 10: Operations on empty book"""
    print("=" * 60)
    print("TEST 10: Empty Book Operations")
    print("=" * 60)
    
    book = OrderBook("TEST10")
    
    assert book.bestBid() is None, "Empty book should have no best bid"
    assert book.bestAsk() is None, "Empty book should have no best ask"
    
    # Market order on empty book
    print("Expecting warning message:")
    book.placeOrder(isBuy=True, isMarket=True, qty=10)
    assert len(book.tradeHistory) == 0, "No trades should occur"
    
    print("✅ PASSED: Empty book handled correctly")
    print()


def test_same_price_buy_sell():
    """Test 11: Multiple orders at same price on both sides"""
    print("=" * 60)
    print("TEST 11: Same Price on Both Sides")
    print("=" * 60)
    
    book = OrderBook("TEST11")
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=10)
    book.placeOrder(isBuy=True, isMarket=False, price=100, qty=15)
    book.placeOrder(isBuy=False, isMarket=False, price=100, qty=20)  # Should match both
    
    assert len(book.tradeHistory) == 2, "Should have 2 trades"
    assert book.tradeHistory[0].qty == 10, "First trade: 10 units"
    assert book.tradeHistory[1].qty == 10, "Second trade: 10 units (partial)"
    
    # 5 units should remain on buy side
    remaining = list(book.orders.values())[0].val
    assert remaining.isBuy == True, "Remaining should be buy order"
    assert remaining.qty == 5, f"Should have 5 remaining, got {remaining.qty}"
    
    print("✅ PASSED: Same price matching works correctly")
    print()


def test_stress_test():
    """Test 12: Stress test with many orders"""
    print("=" * 60)
    print("TEST 12: Stress Test (100 orders)")
    print("=" * 60)
    
    book = OrderBook("TEST12")
    
    # Add 50 buy orders
    for i in range(50):
        price = 100 - i
        qty = (i % 10) + 1
        book.placeOrder(isBuy=True, isMarket=False, price=price, qty=qty)
    
    # Add 50 sell orders
    for i in range(50):
        price = 101 + i
        qty = (i % 10) + 1
        book.placeOrder(isBuy=False, isMarket=False, price=price, qty=qty)
    
    assert book.bestBid() == 100, "Best bid should be 100"
    assert book.bestAsk() == 101, "Best ask should be 101"
    assert len(book.orders) == 100, "Should have 100 orders"
    book.placeOrder(isBuy=True, isMarket=True, qty = 55)
    book.placeOrder(isBuy=False, isMarket=True, qty = 54)
    assert book.bestAsk() == 111, "Best ask should be 110"
    assert book.bestBid() == 91, "Best bid ask should be 91"
    book.placeOrder(isBuy=False, isMarket=True, qty = 1)
    assert book.bestBid() == 90, "Best bid ask should be 90"
    
    # Large market buy
    book.placeOrder(isBuy=True, isMarket=True, qty=100)
    
    print(f"✅ PASSED: Processed 100+ orders, {len(book.tradeHistory)} trades executed")
    print()


def run_all_tests():
    """Run all test cases"""
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE ORDER BOOK TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        test_basic_limit_orders,
        test_immediate_matching,
        test_fifo_matching,
        test_market_order_buy,
        test_market_order_partial_fill,
        test_order_cancellation,
        test_partial_fills,
        test_price_improvement,
        test_multiple_price_levels,
        test_empty_book,
        test_same_price_buy_sell,
        test_stress_test
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️  {failed} test(s) need attention")


if __name__ == "__main__":
    # Note: Save your updated order book code as 'order_book_user.py' first
    # Then run this test file
    print("To run tests:")
    print("1. Save your order book code as 'order_book_user.py'")
    print("2. Run: python test_order_book.py")
    print("\nTest scenarios included:")
    print("  • Basic limit orders")
    print("  • Immediate matching")
    print("  • FIFO priority")
    print("  • Market orders")
    print("  • Partial fills")
    print("  • Cancellations")
    print("  • Price improvement")
    print("  • Empty book handling")
    print("  • Stress testing")
    run_all_tests()