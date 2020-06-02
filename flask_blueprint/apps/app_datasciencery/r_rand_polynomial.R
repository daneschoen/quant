
"""
Suppose we want to create a polynomial that can approximate better the following
dataset on the population of a certain Italian city over 10 years.
"""


Year <- c(1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969)
Population <- c(4835, 4970, 5085, 5160, 5310, 5260, 5235, 5255, 5235, 5210, 5175)

sample1 <- data.frame(Year, Population)

"""
For convenience we modify the column Year, creating a neighborhood of zero, thus:
"""
