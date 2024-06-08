# for i in range (4):
#     for j in range (4):
#         print("i = {} and j = {} " .format(i,j))

# for i in range (4):
#     print("mausham")
#     for j in range (4):
#         print("kumar",end = "")
#         for k  in range(4):
#             print("mahato",end = "")


# import random

# def guess(x):
#     random_number = random.randint(1,x)
#     guess =  0
#     while guess != random_number:
#         guess = int (input(f"Guess a number between 1 and {x}"))
#         if guess>random_number:
#             print("You guess too high ")
#         else:
#             print("You guess too low ")
#     print("yahh congrate ..... You guessed right number ")

# def computer_guess(x):
#     low = 1
#     high = x
#     feedback = ""
#     while feedback != "c":
#         if low !=high:
#             guess = random.randint(low,high)
#         else:
#             guess = low
#     feedback = input(f"Is {guess} too high(h) or low(l),or correct(C) !!!".lower())
#     if feedback == "h" :
#         guess = high-1 
#     elif feedback =="l":
#         guess = low+1

#     print("yahh ... you guessed right number ") 

# print(computer_guess(20))


# class Car:

#     def __init__(self, speed=0):
#         self.speed = speed
#         self.odometer = 0
#         self.time = 0

#     def accelerate(self):
#         self.speed += 5

#     def brake(self):
#         self.speed -= 5

#     def step(self):
#         self.odometer += self.speed
#         self.time += 1

#     def average_speed(self):
#         return self.odometer / self.time


# if __name__ == '__main__':

#     my_car = Car()
#     print("I'm a car!")
#     while True:
#         action = input("What should I do? [A]ccelerate, [B]rake, "
#                         "show [O]dometer, or show average [S]peed?").upper()
#         if action not in "ABOS" or len(action) != 1:
#             print("I don't know how to do that")
#             continue
#         if action == 'A':
#             my_car.accelerate()
#             print("Accelerating...")
#         elif action == 'B':
#             my_car.brake()
#             print("Braking...")
#         elif action == 'O':
#             print("The car has driven {} kilometers".format(my_car.odometer))
#         elif action == 'S':
#             print("The car's average speed was {} kph".format(my_car.average_speed()))
#         my_car.step()