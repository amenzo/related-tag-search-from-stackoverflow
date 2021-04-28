import requests
from bs4 import BeautifulSoup
import networkx as nx
import json

pages=10
cleaned_tags_list=[]
tag="android"

def getTags(url, cleaned_tags_list):
    req=requests.get(url)
    result=req.text  #get the result of the request in text format
    sort=BeautifulSoup(result,'lxml')
    list=sort.find_all('p') #getting all the data in the p tags
    string=str(list)  #changing the data to string

    listSplittedInTags=string.split('tags')
    tag_list=[]
    for i in range(1,len(listSplittedInTags)):
        tags=listSplittedInTags[i].split('owner')[0][2:-2]
        tag_list.append(tags)
    clean_tags(tag_list,cleaned_tags_list)

def clean_tags(tag_list, cleaned_tags_list):
    for tags in tag_list:
        tags=tags.split(',')
        temp_list=[] #cleaned tags holder
        for tag in tags:
            temp_list.append(tag.replace('"','').replace('[','').replace(']',''))
        cleaned_tags_list.append(temp_list)

for page in range(1,11):
    url='https://api.stackexchange.com/2.2/questions?page='+str(page)+'&pagesize=100&order=desc&sort=activity&site=stackoverflow'
    getTags(url,cleaned_tags_list)
#print(cleaned_tags_list)

#creating the weighted graph
tag_graph=nx.Graph()
for tag_list in cleaned_tags_list:
    if len(tag_list)==1:
        if tag_list[0] not in list(tag_graph.nodes()):
            tag_graph.add_node(tag_list[0])
    else:
        while(len(tag_list)>1):
            tag=tag_list.pop(0)  #pick a tag_graph
            if tag not in list(tag_graph.nodes()): #checking if it is already added to the graph
                tag_graph.add_node(tag)
            for temp_tag in tag_list:
                if(tag,temp_tag) not in tag_graph.edges([tag]): #checkking if it there is an edge between the two tags
                    tag_graph.add_edge(tag,temp_tag,weight=1) #initialize with one if not initialized
                else:
                    tag_graph[tag][temp_tag]['weight']+=1
        if tag_list[0] not in list(tag_graph.nodes()): #adding the last node to the graph if not present
            tag_graph.add_node(tag_list[0])

#store the graph in to a reusable dictionary
serialized_graph=nx.readwrite.json_graph.node_link_data(tag_graph)

#get the nodes only from the serialized_graph
nodes=serialized_graph['nodes']

#get the edges only from the serialized_graph
edges=serialized_graph['links']

#save the nodes to nodes.txt and the edges to edges.txt
with open('nodes.txt','w') as outfile:
    json.dump(nodes,outfile)
with open('edges.txt','w') as outfile:
    json.dump(edges,outfile)
