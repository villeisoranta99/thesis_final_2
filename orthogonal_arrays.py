"""
Generates the orthogonal arrays for the experimental design discussed
in Section 3.1.5.
Ville Isoranta / 17.7.2025
"""
import oapackage
import tempfile

"""
Defines the orthogonal array to be generated.
"""
run_size = 27
strength = 2
number_of_factors = 7
factor_levels = 3
arrayclass = oapackage.arraydata_t(factor_levels, run_size, strength, number_of_factors)
print(arrayclass)

"""
Generation of a 27 run root array.
"""
ll2 = [arrayclass.create_root()]
ll2[0].showarraycompact()

"""
Generates the different orthogonal
arrays available.
"""
list3columns = oapackage.extend_arraylist(ll2, arrayclass)
print("extended to %d arrays with 3 columns" % len(list3columns))

list4columns = oapackage.extend_arraylist(list3columns, arrayclass)
print("extended to %d arrays with 4 columns" % len(list4columns))

list5columns = oapackage.extend_arraylist(list4columns, arrayclass)
print("extended to %d arrays with 5 columns" % len(list5columns))

list6columns = oapackage.extend_arraylist(list5columns, arrayclass)
print("extended to %d arrays with 6 columns" % len(list6columns))

list7columns = oapackage.extend_arraylist(list6columns, arrayclass)
print("extended to %d arrays with 7 columns" % len(list7columns))

"""
Then the arrays are saved into a file.
"""
filename = tempfile.mkstemp(".oa")
_ = oapackage.writearrayfile(filename, list7columns, oapackage.ATEXT)
oapackage.oainfo(filename)

