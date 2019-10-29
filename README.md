Dear Insight Team,
  Thanks for letting me do this challenge. It's been a blast, and I've learned
  a lot! Throughout the challenge, I tried different data structures, algorithms,
  and approaches, only to find a better one when I was about 3/4 done. Finally, though,
  I was able to find an approach, set of structures, and algorithm that will
  allow me to process the full data set before the heat death of the universe
  (in fact, I believe it does so in under a minute!) Anyway, here is my final approach:

1. Get data of interest from input CSV file and transfer that to a list object.
2. Transfer list to dictionary to sum up overlapping values (and for easy access later).
3. From dictionary, create a new list with all of the input data consolidated.
4. For each item in the dictionary, add two new items to their corresponding list:__
a: A running average (needed for output file later)__
b: A counter for how many times we've seen this kind of border crossing at this border previously, (needed for updating running average)
5. Get rid of the counter for each border crossing datum
6. Output our results to the output CSV!
