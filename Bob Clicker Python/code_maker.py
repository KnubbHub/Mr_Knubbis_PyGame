import secrets
import random
# import time

coupon = open("codes.txt", "a")

def generate(amount):
    for x in range(amount):
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "1234567890"

        pwd = ''
        for i in range(3):
            for i in range(5):
                pwd += ''.join(secrets.choice(characters))
            for i in range(1):
                pwd += ''.join("-")

        randOpt1 = 1000
        randOpt2 = 1500
        randOpt3 = 2000
        randOpt4 = 2500
        randOpt5 = 3000
        randOpt6 = 3500
        randOpt7 = 4000
        randOpt8 = 4500
        randOpt9 = 5000
        randOpt10 = 5500
        randOpt11 = 6000
        randOpt12 = 6500
        randOpt13 = 7000
        randOpt14 = 7500
        randOpt15 = 8000
        randOpt16 = 8500
        randOpt17 = 9000
        randOpt18 = 9500
        randOpt19 = 9999
        pwd += ''.join(str(random.choice([randOpt1, randOpt2, randOpt3, randOpt4, randOpt5, randOpt6, randOpt7, randOpt8, randOpt9, randOpt10, randOpt11, randOpt12, randOpt13, randOpt14, randOpt15, randOpt16, randOpt17, randOpt18, randOpt19])))

        coupon.write(pwd)
        coupon.write("\n")

    coupon.close()
    coupon1 = open("codes.txt", "r")
    d = coupon1.read()
    coupon1.close()
    m = d.split("\n")
    s = "\n".join(m[:-1])
    coupon2 = open("codes.txt", "w+")
    for i in range(len(s)):
        coupon2.write(s[i])

def delete_all():
    coupon.truncate(0)

# stop = False
# while not stop:
#     generate(100)
#     time.sleep(3600)
#     coupon = open("codes.txt", "a")
#     delete_all()

generate(5)