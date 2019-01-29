# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 16:16
# @Author  : 昨夜
# @Email   : 903165495@qq.com


def isMatch(s, p):
    k=0
    j=0
    while True:
        if j > len(s) - 1:
            return True
        if k > len(p) - 1 and j <= len(s) - 1:
            return False
        if p[k] == s[j]:
            k=k+1
            j=j+1
        elif p[k] == '*':
            if s[j]==s[j-1]:
                while True:

                    if j+1>len(s)-1:
                        return True
                    elif s[j]==s[j+1]:
                        j=j+1
                    if s[j]!=s[j+1]:
                        j=j+1
                        k=k+1
                        break
            else:
                return False

        elif p[k]=='.' :
            if k >= len(p) - 1 :
                k = k + 1
                j = j + 1
            elif p[k + 1] == '*':
                if k + 1 >= len(p)-1:
                    return True
                else:
                    while True:
                        j=j+1
                        if s[j]==p[k + 2]:
                            k=k+2
                            break
                        if j>len(s)-1:
                            return False



            else:
                k = k + 1
                j = j + 1






if __name__ == '__main__':
    s="aaaa"
    p="a*"
    print(isMatch(s, p))