import hashlib
import collections
from dataclasses import dataclass


class Node(object):
    def __init__(self, val=None, left=None, right=None):
        # Hash value of the node via hashlib.sha256(xxxxxx.encode()).hexdigest()
        self.val = val
        # Left node
        self.left = left
        # Right node
        self.right = right

    def __str__(self):
        return f':val={self.val},left={self.left},right={self.right}:'


class MerkleTrees(object):
    def __init__(self):
        self.root = None
        # txns dict: { hash_val -> 'file_path' }
        self.txns = None

    def get_root_hash(self):
        return self.root.val if self.root else None

    def build(self, txns):
        """
        Construct a Merkle tree using the ordered txns from a given txns dictionary.
        """
        # save the original txns(files) dict while building a Merkle tree.
        self.txns = txns
        txns_list = list(txns.keys())
        if len(txns_list) % 2 != 0:
            txns_list.append(txns_list[-1])
        queue = collections.deque()
        for index in range(0, len(txns_list)-1, 2):
            left = txns_list[index]
            right = txns_list[index+1]
            combine = left + right
            root = hashlib.sha256(combine.encode()).hexdigest()
            current_node = Node(root, Node(left), Node(right))
            queue.append(current_node)

        while(len(queue) > 1):
            left = queue.popleft()
            right = queue.popleft()
            combine = left.val+right.val
            root = hashlib.sha256(combine.encode()).hexdigest()
            current_node = Node(root, left, right)
            queue.append(current_node)

        self.root = queue.popleft()

    def print_level_order(self):
        """
          1             1
         / \     -> --------------------    
        2   3       2 3
        """

        height = self.height(self.root)

        for i in range(1, height+1):
            self.print_given_level(self.root, i)
            print('\n-------------------')

    def height(self, node):
        if node is None:
            return 0
        else:
            lheight = self.height(node.left)
            rheight = self.height(node.right)
            return max(lheight, rheight)+1

    def print_given_level(self, root, level):
        if root is None:
            return
        if level == 1:
            print(root.val, end=' ')
        else:
            self.print_given_level(root.left, level-1)
            self.print_given_level(root.right, level-1)

    @staticmethod
    def compare(x, y):
        """
        Compare a given two merkle trees x and y.
        x: A Merkle Tree
        y: A Merkle Tree
        Pre-conditions: You can assume that number of nodes and heights of the given trees are equal.

        Return: A list of pairs as Python tuple type(xxxxx, yyyy) that hashes are not match.
        https://realpython.com/python-lists-tuples/#python-tuples
        """
        diff = []
        if x.get_root_hash() == y.get_root_hash():
            return diff

        compareQueue = collections.deque()
        compareQueue.append(x.root)
        compareQueue.append(y.root)

        while(len(compareQueue) > 1):
            xNode = compareQueue.popleft()
            yNode = compareQueue.popleft()

            if(xNode.val != yNode.val):
                diff.append((xNode.val, yNode.val))

            if xNode.left != None and yNode.left != None:
                compareQueue.append(xNode.left)
                compareQueue.append(yNode.left)
            if xNode.right != None and yNode.right != None:
                compareQueue.append(xNode.right)
                compareQueue.append(yNode.right)
        return diff
