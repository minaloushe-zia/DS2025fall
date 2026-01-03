import random
import sys
import heapq
import timeit

# 增加递归深度限制，防止深度过大的 BST 导致报错
sys.setrecursionlimit(200000)

# Class Definitions (Fixed from PDF) 

class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self._root = None

    def get(self, key):
        return self._get(self._root, key)

    def _get(self, x, key):
        if x is None:
            return None
        if key == x.key:
            return x.key
        elif key < x.key:
            return self._get(x.left, key)
        else:
            return self._get(x.right, key)

    # 插入元素
    def put(self, key):
        self._root = self._put(self._root, key)

    def _put(self, x, key):
        if x is None:
            return Node(key)
        if key < x.key:
            x.left = self._put(x.left, key)
        elif key > x.key:
            x.right = self._put(x.right, key)
        return x

    # 计算树的高度
    def height(self):
        return self._height(self._root)
    
    def _height(self, x):
        if x is None:
            return 0
        return 1 + max(self._height(x.left), self._height(x.right))

class MaxPQ:
    def __init__(self):
        self._pq = []  

    def insert(self, key):
        # 存储 -key 来模拟最大堆
        heapq.heappush(self._pq, -key)

    def contains(self, key):
        return -key in self._pq
    
    # 获取最大值 (堆顶)
    def get_max(self):
        if not self._pq: return None
        return -self._pq[0] 

#  Experiment Setup 

my_id = 42453034  
N = 100000         
print(f"Building data structures with N={N} random integers...")

lst = [i for i in range(N)]
random.shuffle(lst)

bst = BST()
pq = MaxPQ()

# 1. 插入数据 
for item in lst:
    bst.put(item)
    pq.insert(item)

# 2. 插入目标最大值 (my_id)
# my_id 远大于 range(100000)，所以它一定是最大值
bst.put(my_id)
pq.insert(my_id)

print("Data structures built. Starting performance test...")

# 3. 定义测试操作
def get_max_from_bst():

    bst.get(my_id)

def get_max_from_pq():
    # 在 MaxPQ 中，最大值就在数组索引 0 的位置
    pq.get_max()

# 4. 执行测试 
t_bst = timeit.timeit(get_max_from_bst, number=1000)
t_pq = timeit.timeit(get_max_from_pq, number=1000)

print(f"BST get_max time (1000 runs): {t_bst:.6f} seconds")
print(f"PQ  get_max time (1000 runs): {t_pq:.6f} seconds")

if t_pq > 0:
    print(f"Conclusion: MaxPQ is {t_bst / t_pq:.2f} times faster than BST.")

# 回答 height
print(f"The height of the BST is: {bst.height()}")