# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
        
    def numAt(self, node, sum):
        if node is None:
            return 0
        else:
            num = 1 if node.val == sum else 0
            num += self.numAt(node.left, sum - node.val) 
            num += self.numAt(node.right, sum - node.val) 
            return num    

    def numAtOrBelow(self, node, sum):
        if node is None:
            return 0
        else:
            return self.numAt(node, sum) + self.numAtOrBelow(node.left, sum) + self.numAtOrBelow(node.right, sum)

    def pathSum(self, root: TreeNode, sum: int) -> int:
        return self.numAtOrBelow(root, sum)
