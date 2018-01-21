# The number of bits decides the number of elements that we are going to permute
# Example: 16 bits allow us to form a permutation of 2^16 = 65536 elements
NB_BITS = 16
NB_SPLIT = NB_BITS // 2

# The maximum number that we can map
NB_MAX = 2 ** NB_BITS - 1


# This function will map an input number to a pseudorandom permutation
def map_number(number, prf_params):
    # Make sure that the number doesn't exceed the upper limit
    if not 0 <= number <= NB_MAX:
        print("The input number is not in the range: [0,", NB_MAX, "]")
        exit(-1)

    # Convert the number to binary form
    binary = bin(number)[2:]

    # Pad the binary form with leading 0s to make it of length NB_BITS
    # Note that NB_BITS - len(binary) will never be negative since our input range
    # is restricted to fall between 0 and NB_MAX
    binary = '0' * (NB_BITS - len(binary)) + binary

    # Split the binary representation into left and right halves
    left = binary[:NB_SPLIT]
    right = binary[NB_SPLIT:]

    # Simply copy the bits of right half into new left
    new_left = right

    # The new right is formed by xor-ing left and prf(right)
    new_right = int(left, 2) ^ prf(int(right, 2), prf_params[0], prf_params[1])
    new_right = bin(new_right)[2:]
    new_right = '0' * (NB_SPLIT - len(new_right)) + new_right

    return int(new_left + new_right, 2)


# A pseudorandom function that takes in an input number and calculates a
# pseudorandom output. This function can be replaced with any secure PRF,
# but for the sake of simplicity we're going to use a linear function.
def prf(number, a, b):
    return (number * a + b) % (2 ** NB_SPLIT)


# Create an array that stores the mapping for each input number
mapping = [None] * (NB_MAX + 1)
for i in range(0, NB_MAX + 1):
    # This indicates our mapping progress
    # (helps when we are generating a mapping for a large input domain)
    if i % 10000 == 0:
        print("Mapped: ", i, " numbers - ", i * 100 / NB_MAX, "%", sep='')

    # Find the mapping
    i_map = map_number(i, (43, 37))       # First round
    i_map = map_number(i_map, (43, 37))   # Second round
    i_map = map_number(i_map, (27, 108))  # Third round


    # Ensure we haven't mapped any other number to the same permutation
    if mapping[i_map] is not None:
        print(i_map, "is already mapped:", mapping[i_map], i)
        exit(-1)

    # Ensure that our PRP lies within the range 0...NB_MAX
    if i_map < 0 or i_map > NB_MAX:
        print("The mapping is out of range:", i, i_map)
        exit(-1)

    # Store the mapping in a dictionary
    mapping[i_map] = i

# No collisions / errors found!
print("No collisions found!")
