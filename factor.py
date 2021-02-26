# CIS 473/573
# Homework #4
# Daniel Lowd
# February 2021
#
# TEMPLATE CODE
import itertools

# List of variable cardinalities is global, for convenience.
# NOTE: This is not a good software engineering practice in general.
# However, the autograder code currently uses it to set the variable 
# ranges directly without reading in a full model file, so please keep it
# here and use it when you need variable ranges!
var_ranges = []


#
# FACTOR CLASS -- EDIT HERE!
#

class Factor(dict):
    def __init__(self, scope_, vals_):
        self.scope = scope_
        self.vals = vals_
        # self.stride = [0 for i in range(len(self.scope))]
        self.stride = {}
        # self.scope.sort()
        iter = 1
        for i in self.scope:
            self.stride[i] = iter
            iter = iter * var_ranges[i]

    def __mul__(self, other):
        """Returns a new factor representing the product."""
        # TODO -- PUT YOUR MULTIPLICATION CODE HERE!
        j = 0
        k = 0
        new_scope = self.scope.copy()
        for scope in other.scope:
            if scope not in new_scope:
                new_scope.append(scope)
        new_scope.sort()
        val_range = 1
        for i in new_scope:
            val_range = val_range*var_ranges[i]
        new_vals = [0 for i in range(val_range)]

        assignment = {}
        for l in new_scope:
            assignment[l] = 0
        for i in range(len(new_vals)):
            new_vals[i] = self.vals[j]*other.vals[k]
            for l in new_scope:
                assignment[l] += 1
                if assignment[l] == var_ranges[l]:
                    assignment[l] = 0
                    if l in self.stride:
                        j -= (var_ranges[l] - 1)*self.stride[l]
                    if l in other.stride:
                        k -= (var_ranges[l] - 1)*other.stride[l]
                else:
                    if l in self.stride:
                        j += self.stride[l]
                    if l in other.stride:
                        k += other.stride[l]
                    break
        print("Final: ",new_scope)
        print("Final: ", new_vals)
        return Factor(new_scope, new_vals)

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def __repr__(self):
        """Return a string representation of a factor."""
        rev_scope = self.scope[::-1]
        val = "x" + ", x".join(str(s) for s in rev_scope) + "\n"
        itervals = [range(var_ranges[i]) for i in rev_scope]
        for i,x in enumerate(itertools.product(*itervals)):
            val = val + str(x) + " " + str(self.vals[i]) + "\n"
        return val

def _main():
    global var_ranges
    var_ranges = [2, 2, 2, 2, 3, 3, 5]
    f3 = Factor([1], [4, 5])
    f4 = Factor([1, 2], [2.0, 1.0, 0.5, 0.25])
    f34 = f3 * f4
    print(f34)


if __name__ == "__main__":
    _main()
