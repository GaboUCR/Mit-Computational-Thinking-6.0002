###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    file = open(filename,'r+')
    cows = dict()
    for line in file:
        cow = line.split(',')
        cows[cow[0]] = int(cow[1][0])

    return cows

#print(load_cows('ps1_cow_data.txt'))
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    #get the weights of the Cows
    def sort_list (num_list):
        if (num_list == []):
            return []

        max = 0
        for num in num_list:
            if (num > max):
                max = num
        num_list.remove(max)
        return [max] + sort_list(num_list)

    cows_weight = cows.values()
    cows_weight = sort_list(list(cows_weight))
    cows_taken = list()
    trips = list()
    while len(cows_weight) != 0:
        weights = []
        limit = 10
        for weight in cows_weight:
            #given that cows_weight is sorted we start with the heaviest cows and only add them if there is enough space
            if (weight <= limit):
                weights.append(weight)
                limit -= weight
        #select the cows with corresponding weight and add them to the trip
        trip = []
        for cow in cows:
            #check if we haven't taken a that cow since they can share the weight value
            if (cows[cow] in weights and cow not in cows_taken):
                trip.append(cow)
                weights.remove(cows[cow])
                cows_weight.remove(cows[cow])
                cows_taken.append(cow)

        trips.append(trip)

    return trips


#print(greedy_cow_transport(load_cows('ps1_cow_data.txt')))


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cows_names = cows.keys()
    best_trips = [[cow] for cow in cows_names]
    for trip in get_partitions(cows_names):
        #check if the partition includes every cow and if it doesn't surpass the constraint
        possible_trip = True
        n_cows = 0
        cows_weight = 0
        for mod_cows in trip:
            for cow in mod_cows:
                cows_weight += cows[cow]

            if (cows_weight > limit):
                possible_trip = False
            cows_weight = 0
            n_cows += len(mod_cows)
        #Check if every cow is included
        if (n_cows < len(cows_names)):
            possible_trip = False
        #Skip the trips if one of the trips has an unsustainable weight or the partition doesn't include all cows
        if (not possible_trip):
            continue
        #Compare the number of travels with the current best trip or add the trip if it is equal
        if (len(trip) < len(best_trips)):
            best_trips = trip


    return best_trips


print(brute_force_cow_transport(load_cows('ps1_cow_data.txt')))
# Problem 4

def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start_brute_force = time.time()
    brute_force = brute_force_cow_transport(load_cows('ps1_cow_data.txt'))
    end_brute_force = time.time()
    total_time = end_brute_force-start_brute_force
    print('The brute force algorithm took ',total_time,'seconds and found ',len(brute_force),' trips')
    #test greedy
    start_greedy = time.time()
    greedy = greedy_cow_transport(load_cows('ps1_cow_data.txt'))
    end_greedy = time.time()
    total_time = end_greedy-start_greedy
    print('The greedy algorithm took ',total_time,'seconds and found ',len(greedy),' trips')

#compare_cow_transport_algorithms()
