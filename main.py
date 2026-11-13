import math, queue
from collections import Counter

####### Problem 1 #######

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return C

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        # TODO
        x = p.get()
        y = p.get()
        z = TreeNode(x,y,(x.data[0] + y.data[0], ""))
        p.put(z)
        pass
        
    # return root of the tree
    return p.get()

# Perform a traversal on the prefix code tree to collect all encodings.
# Recursively call get_code, appending 0 or 1 to prefix as appropriate
# depending on if the call is to the left or right child.
# When a leaf is found, update the code dict object to map from
# the value in the leaf to the encoding specified by prefix.
# Return the code object.
def get_code(node, prefix="", code={}):
    # TODO - perform a tree traversal and collect encodings for leaves in code
    if code is None:
        code = {}
    if node is None:
        return code
    if node.left is None and node.right is None:
        code[node.data[1]] = prefix
    else:
        if node.left:
            get_code(node.left, prefix + "0", code)
        if node.right:
            get_code(node.right, prefix + "1", code)
    return code
    pass

# Given an alphabet and frequencies, compute the cost of a fixed length encoding.
# You'll have to consider the total number of unique elements in f to 
# determine the number of bits needed to represent each character.
def fixed_length_cost(f):
    # TODO
    if not f:
        return 0
    num_chars = len(f) #length of dictionary keys
    bits_per_char = math.ceil(math.log2(num_chars)) if num_chars > 1 else 1
    total_chars =sum(f.values()) #sum of all the frequencies
    return total_chars * bits_per_char
    pass

# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    # TODO
    total = 0
    for char, freq in f.items():
        if char in C:
            total += freq*len(C[char])
    return total
    pass

def analyze_files():
    for fname in ['alice29.txt', 'asyoulik.txt', 'f1.txt', 'fields.c', 'grammar.lsp']:
        f = get_frequencies(fname)
        print("Fixed-length cost:  %d" % fixed_length_cost(f))
        T = make_huffman_tree(f)
        C = get_code(T)
        print("Huffman cost:  %d" % huffman_cost(C, f))


####### Problem 4 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('relevant', 'elephant')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant')]

def MED(S, T):
    # TODO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(
                MED(S, T[1:]),       # Insertion
                MED(S[1:], T),       # Deletion
                MED(S[1:], T[1:])    # Substitution
            ))

def fast_MED(S, T):
    # TODO -  implement bottom-up memoization
    m, n = len(S), len(T)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S[i-1] == T[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i][j-1],    # Insertion
                    dp[i-1][j],    # Deletion
                    dp[i-1][j-1]   # Substitution
                )
                
    return dp[m][n]
    pass

def fast_align_MED(S, T):
    # TODO - implement bottom-up memoization, allowing
    # for traceback of alignment
    # returns the two alignments (see test_align)
    m, n = len(S), len(T)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 1. Initialize the DP table
    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    # 2. Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S[i-1] == T[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # Deletion
                    dp[i][j-1],    # Insertion
                    dp[i-1][j-1]   # Substitution
                )

    # 3. Traceback
    i, j = m, n
    align_s = []
    align_t = []

    while i > 0 or j > 0:

        # Exact match
        if i > 0 and j > 0 and S[i-1] == T[j-1] and dp[i][j] == dp[i-1][j-1]:
            align_s.append(S[i-1])
            align_t.append(T[j-1])
            i -= 1
            j -= 1

        # Deletion
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            align_s.append(S[i-1])
            align_t.append('-')
            i -= 1

        # Insertion
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            align_s.append('-')
            align_t.append(T[j-1])
            j -= 1

        # Substitution
        else:
            align_s.append(S[i-1])
            align_t.append(T[j-1])
            i -= 1
            j -= 1

    return "".join(reversed(align_s)), "".join(reversed(align_t))
    pass

