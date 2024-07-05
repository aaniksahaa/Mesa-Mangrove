from t import * 
from t2 import * 

a = A('I am A')
a.add_b(B('I am B', a))

a.show()
