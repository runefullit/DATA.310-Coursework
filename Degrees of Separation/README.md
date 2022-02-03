# Decrees of Separation thoughts
  In this exercise the student wrote the missing shortest_path(source, target). I had two main takeaways from this. First, it gave a good idea of when buildling your own class for adata management is useful. And second, that checking for an element's existence should be planned around.
  
  util.py has implementation for checking if one of its elements has a given field value. As it turns out, using the full dataset available here this is an incredibly slow way of checking it with execution times exceeding my patience. Simply omitting these checks and letting the function add redundant information for itself to later check boosted the proogram's performance greatly.
  
  Next I tried saving the checked actor IDs in a list and using the _in_ operation to check if elements are contained. This once again sped up the code by approximately 50% compared to not checking at all. Ultimately saving the checked actor IDs in a set and using the _in_ operation on that proved to be by far the fastest solution, only taking around 2,5% of the time it took with a list.
