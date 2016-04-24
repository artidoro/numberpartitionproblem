__author__ = 'nishaswarup'

import structures
from random import random, sample
from math import exp, floor
from time import time


'''
The order of this file is
    - KK Algorithm
    - Functions for Representation 1
    - Functions for Representation 2
    - Functions for the 3 algorithms
    - Functions for Testing
'''

def KK(nums):
    '''
    This function runs the KK algorithm on the list nums
    It builds a max-heap from the numbers, pops the largest 2
    numbers, then pushes their difference. It does this until
    the heap has size 1, and then it returns that value.
    This is O(n*log(n)) time. Building the heap is a lot of pushes,
    which is log(n) for each heap, so n*log(n) total. Then, popping
    is log(n, and so is pushing. We do each of those 3N times, so we
    get another O(n*log(n)). So the overall algorithm is O(n*log(n))
    :param nums: a list of numbers
    :return: A single value, which is the result of the KK algorithm
    '''

    # first we construct the heap
    heap = []
    for x in nums:
        structures.heap_push(heap, x)
    # now we've constructed the heap, now we loop through
    # and replace the largest two elements with their difference
    while len(heap) > 1:
        biggest = structures.heap_pop(heap)
        biggest2 = structures.heap_pop(heap)
        structures.heap_push(heap, biggest - biggest2)
    return heap[0]

'''
    ****** Representation 1 *******
    *  The below functions are all for the first representation, where
    *  we generate solutions that are alternating -1 and 1
    *******************************
'''

def calculate_residue_1(nums, solution):
    '''
    This function calculates the residue for a given solution
    :param nums: A list of numbers that we're trying to find the parition of
    :param solution: A list of -1 and 1
    :return: A number which represents the residue
    '''
    sum = 0
    for index, value in enumerate(nums):
        sum += value*solution[index]
    return abs(sum)

def generate_random_soln_1(nums):
    '''
    This function generates a random solution for the first representation
    So, it just returns a list of -1 and 1 that is the same length as nums
    :param nums: A list of numbers
    :return: A list of -1 and 1
    '''
    out = []
    for x in xrange(len(nums)):
        if random() < .5:
            out.append(-1)
        else:
            out.append(1)
    return out

def random_move_1(soln):
    '''
    This function makes a random move on the given solution. It retuns
    an array of swaps to make in this random move. For example, it could
    return [[5, 1, -1], [4, -1, 1]]
    Which would indicate we should change position 5 from 1 to -1 and position 4 from -1 to 1.
    The reason we use this strange notation is to make it integrate  with random_move_2
    :param soln: a list of -1 or 1
    :return: An array, look above
    '''
    # Generating two random integers within a range 
    try:
        [i,j] = sample(range(0, len(soln)), 2)
    except ValueError:
        print('Given solution is too short')

    # now i and j are two random numbers s.t. i != j
    out = [[i, soln[i], soln[i]*-1]]
    if random() < .5:
        out.append([j, soln[j], soln[j]*-1])
    return out


'''
    ****** Representation 2 *******
    *  The below functions are all for the second representation, where
    *  we generate solutions that group numbers together
    *******************************
'''

def calculate_residue_2(nums, soln):
    '''
    This calculates the residue for a solution in representation 2.
    :param nums: A list of numbers
    :param soln: A solution in representation 2, sequence representing a partitioning
    :return: A number that represents the residue
    '''

    for i in range(len(soln)):
        if nums[i] != 0:
            for j in range(i+1,len(soln)):
                if soln[i] == soln[j]:
                    nums[i] += nums[j]
                    nums[j] = 0
    return KK(nums)







def generate_random_soln_2(nums):
    '''
    We generate a random solution for the second representation.
    This is just a list of numbers from 0 to len(nums)
    :param nums: A list of numbers
    :return: A list of numbers of the same size as nums
    '''
    out = []
    for x in xrange(len(nums)):
        out.append(int(random()*len(nums)))
    return out


def random_move_2(soln):
    '''
    This function makes a random move on the given solution. It retuns
    an array of swaps to make in this random move. For example, it could
    return [[5, 2, 5]]
    Which would indicate we should change the parameter of position 5 from 2 to 5.
    The reason we use this strange notation is to make it integrate with random_move_1
    :param soln: a list of parameters
    :return: An array, look above
    '''
    # Generating two random integers
    i = int(random()*len(soln))
    j = int(random()*len(soln))
    # handle short solution
    assert len(soln) is not 1, "the given solution is too short"
    while(soln[i] == j):
        j = int(random()*len(soln))

    # now i and j are two random numbers s.t. i != j
    return [[i, soln[i], j]]







'''
    ****** 3 algorithms *******
    *  The below functions are the 3 algorithms we needed to implement
    ***************************
'''
def repeated_random(nums, max_iter, generate_soln, find_residue):
    '''
    This function runs the first algorithm given, where we
    find lots of random solutions and take the best one
    :param nums: The list of numbers we're finding the number partition for
    :param max_iter: The number we're iterating to
    :param generate_soln: A function for generating random solutions (this varies for represenations 1 and 2)
    :param find_residue: A function for calculating the residue of a solution (again, varies per representation)
    :return: Soln, residue. Solution is a list of numbers, residue is the best residue
    '''
    # generate a random solution
    best_soln = generate_soln(nums)
    best_residue = find_residue(nums, best_soln)
    # we loop through lots of times, and return the
    # best random solution
    for x in xrange(max_iter):
        soln = generate_soln(nums)
        residue = find_residue(nums, soln)
        if residue < best_residue:
            best_residue = residue
            best_soln = soln
    return best_soln, best_residue

def hill_climb(nums, max_iter, generate_soln, find_residue, find_neighbor):
    '''
    This function runs the second algorithm, where we find a random solution,
    and then make local improvements.
    :param nums: The list of numbers we're trying to find the partition for
    :param max_iter: The number we're iterating to
    :param generate_soln: A function used to generate a random solution
    :param find_residue: A function used to calculate a residue
    :param find_neighbor: A function that finds a random neighbor. Should be either random_move_1 or random_move_2
    :return: Soln, residue. Solution is a list of numbers, residue is the best residue
    '''
    best_soln = generate_soln(nums)
    best_residue = find_residue(nums, best_soln)
    for x in xrange(max_iter):
        # find the moves we should make to get to a random neighbor
        moves = find_neighbor(best_soln)
        # make these moves
        for move in moves:
            best_soln[move[0]] = move[2]
        residue = find_residue(nums, best_soln)
        # if this was a good move, we keep it
        if residue < best_residue:
            best_residue = residue
        # otherwise we revert
        else:
            for move in moves:
                best_soln[move[0]] = move[1]
    return best_soln, best_residue


def simul_anneal(nums, max_iter, generate_soln, find_residue, find_neighbor):
    '''
    This function runs the third algorithm, where we find a random solution,
    and then try to improve it, we don't always move to better neighbors 
    :param nums: The list of numbers we're trying to find the partition for
    :param max_iter: The number we're iterating to
    :param generate_soln: A function used to generate a random solution
    :param find_residue: A function used to calculate a residue
    :param find_neighbor: A function that finds a random neighbor. Should be either random_move_1 or random_move_2
    :return: Soln, residue. Solution is a list of numbers, residue is the best residue
    '''
    best_soln = cur_soln = generate_soln(nums)
    best_residue = cur_residue = find_residue(nums, cur_soln)
   
  #  print "cur sol =", cur_soln, "cur res =", cur_residue
    for x in xrange(max_iter):
        # initialize neighbor from current solution
        neighbor = cur_soln
        # find the moves we should make to get to a random neighbor
        moves = find_neighbor(cur_soln)
        # make these moves
        for move in moves:
            neighbor[move[0]] = move[2]
        neighbor_residue = find_residue(nums, neighbor)
        #print "neighbor =", neighbor, "neighbor_residue =", neighbor_residue
        # if this was a good move, we keep it
        if neighbor_residue < cur_residue:
            cur_soln = neighbor
            cur_residue =  neighbor_residue
         #   print "neighbor was better"
        # otherwise we keep it with some probability
        else:
            if random()  < exp(-(neighbor_residue-cur_residue)/T(x)):
                cur_soln = neighbor
                cur_residue =  neighbor_residue
          #      print "switched to worst sol"
        #print "cur sol =", cur_soln, "cur res =", cur_residue
        # we will always return the best solution seen so far, so we store it
        if cur_residue < best_residue:
            best_soln = cur_soln
            best_residue =  cur_residue
    return best_soln, best_residue


def T(iter):
    '''
    This function determines the cooling schedule. It affects the probability of keeping
    a worst solution in the simulated annealing function. We are using the function 
    given in the prompt.
    '''    
    return (10**10) * (0.8)**(floor(iter/300.))



'''
    ****** Testing *******
    *  The below functions are all for testing
    **********************
'''
def generate_random_instance():
    '''
    This returns a list of 100 numbers, with each number being chosen from [1, 10**12]
    This specification is given in the assignment
    :return: A list of numbers
    '''
    out = []
    for x in xrange(100):
        out.append( int(random()*(10**12)) + 1 )
    return out

def test_instance(max_iter,nums):
    '''
    This function tests one instance with the KK algorithm, a repeated random algorithm,
    a hill climbing algorithm, and a simulated annealing algorithm for 25,000 iterations.
    :param max_iter: how many iterations we should run
    :return: Notihg, for now
    '''
    # generate instance
    instance = nums #generate_random_instance()
    # KK algorithm
    print "KK Algorithm"
    start_time = time()
    KK_ans = KK(instance)
    KK_time = time() - start_time
    print "\t\tResult:\t" + str(KK_ans)
    print "\t\tTime:\t" + str(KK_time) + "s"
    # Run Representation 1 Algorithm
    print "Representation 1:"
    # repeated random
    print "\tRepeated Random"
    start_time = time()
    temp,R1_RR_ans = repeated_random(instance, max_iter, generate_random_soln_1, calculate_residue_1)
    R1_RR_time = time() - start_time
    print "\t\tResult:\t" + str(R1_RR_ans)
    print "\t\tTime:\t" + str(R1_RR_time)
    # hill climbing
    print "\tHill Climbing"
    start_time = time()
    temp, R1_HC_ans = hill_climb(instance, max_iter, generate_random_soln_1, calculate_residue_1, random_move_1)
    R1_HC_time = time() - start_time
    print "\t\tResult:\t" + str(R1_HC_ans)
    print "\t\tTime:\t" + str(R1_HC_time) + "s"

    # simulated annealing 
    print "\tSimulated Annealing"
    start_time = time()
    temp, R1_HC_ans = simul_anneal(instance, max_iter, generate_random_soln_1, calculate_residue_1, random_move_1)
    R1_HC_time = time() - start_time
    print "\t\tResult:\t" + str(R1_HC_ans)
    print "\t\tTime:\t" + str(R1_HC_time) + "s"

    # Run Representation 2 Algorithm
    print "Representation 2:"
    # repeated random
    print "\tRepeated Random"
    start_time = time()
    temp,R1_RR_ans = repeated_random(instance, max_iter, generate_random_soln_2, calculate_residue_2)
    R1_RR_time = time() - start_time
    print "\t\tResult:\t" + str(R1_RR_ans)
    print "\t\tTime:\t" + str(R1_RR_time)
    # hill climbing
    print "\tHill Climbing"
    start_time = time()
    temp, R1_HC_ans = hill_climb(instance, max_iter, generate_random_soln_2, calculate_residue_2, random_move_2)
    R1_HC_time = time() - start_time
    print "\t\tResult:\t" + str(R1_HC_ans)
    print "\t\tTime:\t" + str(R1_HC_time) + "s"

    # simulated annealing 
    print "\tSimulated Annealing"
    start_time = time()
    temp, R1_HC_ans = simul_anneal(instance, max_iter, generate_random_soln_2, calculate_residue_2, random_move_2)
    R1_HC_time = time() - start_time
    print "\t\tResult:\t" + str(R1_HC_ans)
    print "\t\tTime:\t" + str(R1_HC_time) + "s"

def test_calculate_residue_2 ():
    '''
    This function tests a small number of cases for which the solution has been 
    calculated by hand
    :param: nothing for now
    :return: boolean, true if it passes the tests
    '''
    nums = [10,8,7,6,5]
    soln = [1,2,2,4,5]
    return 4 == calculate_residue_2(nums,soln)


def get_nums_file(infile):
    infile = open(infile)
    nums = []
    for line in infile:
        nums.append(line)
    nums = [int(i) for i in nums]
    infile.close()  
    return nums



test_instance(25000,get_nums_file('input.txt'))
#test_calculate_residue_2()
#print simul_anneal([10,8,7,6,5], 100, generate_random_soln_2, calculate_residue_2, random_move_2)
