class HeapQueue:

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
            print("Entry with key", key, "already exists")
            return False
        self.heap.append((key,value))
        n = len(self.heap)
        self.positions[key] = n-1
        self.upheap(n-1)
        # print(self)
        return True
    
    def pop(self):
        if not self.heap: return None
        key, value = self.heap[0]
        self.remove(key)
        return key, value

    def remove(self, key):
        if not self.isIn(key):
            return None
        pos = self.positions[key]
        lastPos = len(self.heap)-1
        self.swap(pos,lastPos)
        self.heap.pop()
        del self.positions[key]
        # upheap / downheap
        if pos < len(self.heap):
            if pos > 0 and self.heap[pos][0] < self.heap[(pos-1)//2][0]:
                self.upheap(pos)
            else:
                self.downheap(pos)
        # print(self)

    def upheap(self, pos: int):
        while pos > 0 and self.heap[(pos-1)//2][0] > self.heap[pos][0]:
            self.swap(pos,(pos-1)//2)
            pos = (pos-1) // 2

    def downheap(self, pos: int):
        childPos = self.minChildPos(pos)
        while childPos is not None and self.heap[pos][0] > self.heap[childPos][0]:
            self.swap(pos,childPos)
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
        if c1 >= len(self.heap): return None
        if c2 >= len(self.heap): return c1
        if self.heap[c1][0] <= self.heap[c2][0]:
            return c1
        return c2
    
    def __str__(self):
        return str(self.heap) #+" "+str(self.positions)
    
    def __bool__(self):
        return len(self.heap) > 0
    
    def __len__(self):
        return len(self.heap)

    def verify_heap_property(self):
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
        for key, pos in self.positions.items():
            if self.heap[pos][0] != key:
                return False
        return True