"""
HeapQueue Stress Test
=====================
Tests correctness under heavy load and edge cases.
"""

import random
import heapq


class HeapQueue:
    """Copy your implementation here"""
    def __init__(self):
        self.heap = []
        self.positions = {}

    def isIn(self, key):
        return key in self.positions
    
    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]
    
    def get(self, key):
        if not self.isIn(key):
            return None
        return self.heap[self.positions[key]][1]

    def insert(self, key, value = None):
        if self.isIn(key):
            return False
        self.heap.append((key, value))
        n = len(self.heap)
        self.positions[key] = n-1
        self.upheap(n-1)
        return True
    
    def pop(self):
        if not self.heap: 
            return None
        key, value = self.heap[0]
        self.remove(key)
        return key, value

    def remove(self, key):
        if not self.isIn(key):
            return None
        pos = self.positions[key]
        lastPos = len(self.heap) - 1
        
        # Removing last element
        if pos == lastPos:
            self.heap.pop()
            del self.positions[key]
            return
        
        # Swap with last and remove
        self.swap(pos, lastPos)
        self.heap.pop()
        del self.positions[key]
        
        # Fix heap property (might need upheap or downheap)
        if pos < len(self.heap):
            if pos > 0 and self.heap[pos][0] < self.heap[(pos-1)//2][0]:
                self.upheap(pos)
            else:
                self.downheap(pos)

    def upheap(self, pos: int):
        while pos > 0 and self.heap[(pos-1)//2][0] > self.heap[pos][0]:
            self.swap(pos, (pos-1)//2)
            pos = (pos-1) // 2

    def downheap(self, pos: int):
        childPos = self.minChildPos(pos)
        while childPos is not None and self.heap[pos][0] > self.heap[childPos][0]:
            self.swap(pos, childPos)
            pos = childPos
            childPos = self.minChildPos(pos)
    
    def swap(self, pos1, pos2):
        temp = self.heap[pos1]
        self.heap[pos1] = self.heap[pos2]
        self.heap[pos2] = temp
        self.positions[self.heap[pos1][0]] = pos1
        self.positions[self.heap[pos2][0]] = pos2

    def minChildPos(self, pos: int):
        c1 = 2 * pos + 1
        c2 = c1 + 1
        if c1 >= len(self.heap): 
            return None
        if c2 >= len(self.heap): 
            return c1
        if self.heap[c1][0] <= self.heap[c2][0]:
            return c1
        return c2
    
    def __bool__(self):
        return len(self.heap) > 0
    
    def __len__(self):
        return len(self.heap)
    
    def verify_heap_property(self):
        """Check if heap property is maintained"""
        for i in range(len(self.heap)):
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < len(self.heap):
                if self.heap[i][0] > self.heap[left][0]:
                    return False
            if right < len(self.heap):
                if self.heap[i][0] > self.heap[right][0]:
                    return False
        return True
    
    def verify_positions(self):
        """Check if positions dict matches heap"""
        for key, pos in self.positions.items():
            if self.heap[pos][0] != key:
                return False
        return True


def test_basic_operations():
    """Test 1: Basic insert, peek, pop"""
    print("Test 1: Basic Operations")
    
    hq = HeapQueue()
    
    # Insert
    hq.insert(5, "five")
    hq.insert(2, "two")
    hq.insert(8, "eight")
    hq.insert(1, "one")
    
    assert hq.peek()[0] == 1, "Min should be 1"
    assert len(hq) == 4, "Size should be 4"
    
    # Pop
    assert hq.pop()[0] == 1
    assert hq.pop()[0] == 2
    assert hq.pop()[0] == 5
    assert hq.pop()[0] == 8
    assert hq.pop() is None
    
    print("✅ PASSED\n")


def test_remove_operations():
    """Test 2: Remove arbitrary elements"""
    print("Test 2: Remove Operations")
    
    hq = HeapQueue()
    
    # Insert
    for i in [10, 5, 15, 3, 7, 12, 20]:
        hq.insert(i, f"val{i}")
    
    # Remove middle elements
    hq.remove(5)
    assert not hq.isIn(5)
    assert hq.verify_heap_property(), "Heap property violated after remove(5)"
    
    hq.remove(15)
    assert not hq.isIn(15)
    assert hq.verify_heap_property(), "Heap property violated after remove(15)"
    
    # Remove min
    hq.remove(3)
    assert hq.peek()[0] == 7, "After removing 3, min should be 7"
    
    # Remove last
    remaining = [item[0] for item in hq.heap]
    last_key = remaining[-1]
    hq.remove(last_key)
    assert not hq.isIn(last_key)
    assert hq.verify_heap_property()
    
    print("✅ PASSED\n")


def test_duplicate_keys():
    """Test 3: Duplicate key handling"""
    print("Test 3: Duplicate Keys")
    
    hq = HeapQueue()
    
    hq.insert(5, "first")
    result = hq.insert(5, "second")
    
    assert result == False, "Should reject duplicate key"
    assert hq.get(5) == "first", "Original value should remain"
    
    print("✅ PASSED\n")


def test_remove_all():
    """Test 4: Remove all elements one by one"""
    print("Test 4: Remove All Elements")
    
    hq = HeapQueue()
    keys = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35]
    
    for k in keys:
        hq.insert(k, f"val{k}")
    
    # Remove in random order
    random.shuffle(keys)
    
    for k in keys:
        hq.remove(k)
        assert not hq.isIn(k)
        assert hq.verify_heap_property()
        assert hq.verify_positions()
    
    assert len(hq) == 0
    assert hq.pop() is None
    
    print("✅ PASSED\n")


def test_stress_random_operations():
    """Test 5: Random inserts and removes"""
    print("Test 5: Stress Test - Random Operations")
    
    hq = HeapQueue()
    reference = []  # Use Python's heapq as reference
    active_keys = set()
    
    random.seed(42)
    operations = 1000
    
    for i in range(operations):
        # Random operation
        op = random.choice(['insert', 'remove', 'pop'])
        
        if op == 'insert':
            key = random.randint(1, 500)
            if key not in active_keys:
                hq.insert(key, f"val{key}")
                heapq.heappush(reference, key)
                active_keys.add(key)
        
        elif op == 'remove' and active_keys:
            # Remove random element
            key = random.choice(list(active_keys))
            hq.remove(key)
            reference.remove(key)
            heapq.heapify(reference)
            active_keys.remove(key)
        
        elif op == 'pop' and hq:
            result = hq.pop()
            ref_result = heapq.heappop(reference)
            assert result[0] == ref_result, f"Pop mismatch: {result[0]} vs {ref_result}"
            active_keys.remove(result[0])
        
        # Verify invariants
        if i % 100 == 0:
            assert hq.verify_heap_property(), f"Heap property violated at op {i}"
            assert hq.verify_positions(), f"Positions mismatch at op {i}"
            
            # Check min element matches
            if hq and reference:
                assert hq.peek()[0] == reference[0], f"Min mismatch at op {i}"
    
    print(f"✅ PASSED - {operations} random operations\n")


def test_ascending_descending():
    """Test 6: Insert in order (worst case for naive heap)"""
    print("Test 6: Ordered Insertions")
    
    # Ascending
    hq = HeapQueue()
    for i in range(100):
        hq.insert(i, f"val{i}")
    
    assert hq.verify_heap_property()
    assert hq.peek()[0] == 0
    
    # Remove every other element
    for i in range(0, 100, 2):
        hq.remove(i)
    
    assert hq.verify_heap_property()
    assert hq.peek()[0] == 1
    
    # Descending
    hq2 = HeapQueue()
    for i in range(100, 0, -1):
        hq2.insert(i, f"val{i}")
    
    assert hq2.verify_heap_property()
    assert hq2.peek()[0] == 1
    
    print("✅ PASSED\n")


def test_pop_until_empty():
    """Test 7: Pop entire heap"""
    print("Test 7: Pop Until Empty")
    
    hq = HeapQueue()
    keys = random.sample(range(1, 1001), 100)
    
    for k in keys:
        hq.insert(k, f"val{k}")
    
    prev = -1
    count = 0
    while hq:
        key, val = hq.pop()
        assert key > prev, "Elements not in sorted order"
        prev = key
        count += 1
    
    assert count == 100
    assert len(hq) == 0
    assert not hq
    
    print("✅ PASSED\n")


def test_single_element():
    """Test 8: Edge case - single element"""
    print("Test 8: Single Element")
    
    hq = HeapQueue()
    
    hq.insert(42, "answer")
    assert hq.peek()[0] == 42
    assert len(hq) == 1
    
    hq.remove(42)
    assert len(hq) == 0
    assert hq.peek() is None
    
    # Insert and pop
    hq.insert(99, "test")
    result = hq.pop()
    assert result[0] == 99
    assert len(hq) == 0
    
    print("✅ PASSED\n")


def test_large_scale():
    """Test 9: Large scale - 10,000 operations"""
    print("Test 9: Large Scale (10,000 elements)")
    
    hq = HeapQueue()
    
    # Insert 10,000 elements
    keys = list(range(10000))
    random.shuffle(keys)
    
    for k in keys:
        hq.insert(k, f"val{k}")
    
    assert len(hq) == 10000
    assert hq.verify_heap_property()
    assert hq.peek()[0] == 0
    
    # Remove 5,000 random elements
    to_remove = random.sample(keys, 5000)
    for k in to_remove:
        hq.remove(k)
    
    assert len(hq) == 5000
    assert hq.verify_heap_property()
    
    # Pop remaining
    prev = -1
    while hq:
        key, _ = hq.pop()
        assert key > prev
        prev = key
    
    print("✅ PASSED\n")


def test_positions_consistency():
    """Test 10: Positions dict always matches heap"""
    print("Test 10: Positions Consistency")
    
    hq = HeapQueue()
    
    # Many operations
    for i in range(200):
        hq.insert(i, f"val{i}")
    
    # Check positions
    assert hq.verify_positions()
    
    # Remove half
    for i in range(0, 200, 2):
        hq.remove(i)
        assert hq.verify_positions(), f"Positions broken after removing {i}"
    
    # Pop some
    for _ in range(50):
        hq.pop()
        assert hq.verify_positions()
    
    print("✅ PASSED\n")


def run_all_tests():
    """Run complete test suite"""
    print("=" * 60)
    print("HEAPQUEUE STRESS TEST SUITE")
    print("=" * 60 + "\n")
    
    tests = [
        test_basic_operations,
        test_remove_operations,
        test_duplicate_keys,
        test_remove_all,
        test_stress_random_operations,
        test_ascending_descending,
        test_pop_until_empty,
        test_single_element,
        test_large_scale,
        test_positions_consistency,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️  {failed} test(s) failed")


if __name__ == "__main__":
    run_all_tests()