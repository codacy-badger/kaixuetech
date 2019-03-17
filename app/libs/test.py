# -*- coding: utf-8 -*-
# @Time    : 2019/3/8 19:51
# @Author  : 昨夜
# @Email   : 903165495@qq.com

class Solution:
    # matrix类型为二维列表，需要返回列表
    def printMatrix(self, matrix):
        # write code here

        leng=len(matrix)
        if leng==0:
            return []
        if leng==1:
            return matrix[0]
        print(matrix)
        if matrix[0]==[]:
            return []
        lengy = len(matrix[0] )
        if lengy==1:
            a=[]
            for i in matrix:
                a=a+i
            return  a
        #从左到右
        a1=matrix[0]
        # 从上到下
        a2=[]
        # 从下到上
        a4=[]

        for i in range(1,leng-1):
            print(i)
            a2.append(matrix[i][lengy-1])
            a4.append(matrix[i][0])
            matrix[i].remove(matrix[i][lengy - 1])
            matrix[i].remove(matrix[i][0])



        #从 右到左

        a3= list(reversed(matrix[leng-1]))
        a4=list(reversed(a4))

        k=a1+a2+a3+a4

        matrix=matrix[1:-1][:]

        return k+self.printMatrix(matrix)



    def Permutation(self, ss):
        # write code here

        if ss=='':
            return []
        from itertools import product
        l = [i for i in ss]

        data = list(product(l, repeat=len(l)))

        datas=list(set([ ''.join(list(i)) for i in data]))

        return datas


if __name__ == '__main__':
    # Solution().Permutation("aa")
    numbers=[1,1,1,5,1,6,1,3]
    b = sorted(numbers)
    leng = len(b) - 1
    c = b[int(leng / 2)]
    d = b.count(c)
    if d < (leng+1) / 2:
        print(0)
    else:
        print(c)