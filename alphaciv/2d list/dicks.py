class noCity():
    def __init__(self):
        pass

    def willPass(self):
        pass

l = [noCity()]

if isinstance(l[0], noCity):
    print "MMMYES"
