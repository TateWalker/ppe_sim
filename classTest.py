class A:
	height = 2
    # properties of class A

class B(A):
	def __init__(self):
		self.height = 5
	length = 4
	
    # class B inheriting property of class A
    # more properties of class B

class C(B):
	width = 3
    # class C inheriting property of class B
    # thus, class C also inherits properties of class A
    # more properties of class C


test = C()
print(test.height)
print(B.height)