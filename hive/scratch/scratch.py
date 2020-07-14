import json
import math





def checkWinner(codeList, shoppingCart):
    pos = 0
    # while pos < len(shoppingCart):
    for list in codeList:
        cart_pos = 0

        for list_item in list:
            found = False
            for cart_item in shoppingCart[cart_pos:]:
                if cart_item == list_item:
                    print(f"found {cart_item}")
                    found = True
                    break


    return 1
    pass


def inList(list1, list2):
    fail = False
    x = 0
    while x < len(list2):
        fail = False
        for i in range(x, len(list1), 1):
            print(f"fo {i}, {list1[i]}, {x}")
            for i2 in range(len(list2)):
                if list1[i] != list2[i2]:
                    fail = True

                    break
        x += 1

    print(f"i={i}, {fail}, {i2}")
    return not fail


if __name__ == '__main__':
    apple = "apple"
    orange = "orange"
    banana = "banana"
    print(f"... {inList([ apple, apple], [orange, apple, apple, banana, orange, apple, banana])}")



# if __name__ == '__main__':
#     apple = "apple"
#     orange = "orange"
#     banana = "banana"
#     print(f"... {checkWinner([[orange], [apple, apple], [banana, orange, apple], [banana]], [orange, apple, apple, banana, orange, apple, banana])}")

