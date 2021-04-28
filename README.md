# related-tag-search-from-stackoverflow

In here we will try to get some data from stackexchange api and get the related tags with a specific tag provided by the user

To complete this task, we have to follow some steps

1. Connect to stackexchange api and get data from it. For this purpose I will get data from ten pages using the url 'https://api.stackexchange.com/2.2/questions?page=1&pagesize=100&order=desc&sort=activity&site=stackoverflow'

2. Then we create weighted graph using the tags obtained from step one

3. on this step, the graph is serialized into a json dictionary.Nodes and edges and stored a nodes.txt and edges.txt files

4. use the saved text files to get all edges for a give tag and sorted based on its weight.

5. Implement flask app to get the result from step 4 and display them in to a wep-page  
