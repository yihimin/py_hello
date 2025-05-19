class dad():
    def dad_look(self):
        print("handsome")
    def doYouKnow(self, lec) :
        print(f"I don't know {lec}")

class mom():
    def mom_look(self):
        print("pretty")

class child1(dad, mom):
    pass

class child2(dad, mom):
    def doYouKnow(self, lec):
        print(f"I love {lec}")

c1 = child1()
c1.dad_look()
c1.mom_look()
c1.doYouKnow("Python daddy")

c2 = child2()
c2.doYouKnow("Python mommy")