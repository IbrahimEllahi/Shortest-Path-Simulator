# Shortest-Path-Simulator

This program allows users to create their own node maps! Using these node maps you can save the created data and pass it onto a shortest path algorithm (contributed: [@tejveer](https://github.com/tejveeer/)). 

<br>

### Find The Shortest Paths

<br>

![shortest](https://user-images.githubusercontent.com/85767913/152070886-4de6c79f-4b13-4bcb-9619-bc592002fb0e.gif)
### Note: `The keys of the dictionary are in order of the path, for eg: {1:None, 2:None, 3:None} this means that our path starts at 1, then visits 2 and ends at 3`

<br>

### Create Your Own Node Maps

<br>

![create](https://user-images.githubusercontent.com/85767913/152071351-b840e917-9e77-4e17-abb3-ba852505f8e3.gif)


## Controls

<br>

`C` - Create a centered node at mouse cursor position

`F` - Create/delete a line between 2 selected nodes

`R` - Turn Graph Mode on/off

`Q` - Find shortest path between two nodes

`Left Ctrl` - Delete selected node

`Space` - Center all nodes on screen

`S` - Save File

`L` - Load saved graph data

<br>

## Setup

Use `pip install pygame` to install all the necessary packages

<br>

## Functionality

 This path simulator takes advantage of `pygame`'s visuals to produce custom node maps in which the map data can be saved and passed onto a path finding algorithm, allowing users to map out real locations and create a small GPS where they can take 2 places and map out the quickest route between them. Me and my programming team used this software to create a custom map of our school (we received the original map, which is why we were able to make a node version of it), the rooms and hallways were replaced with nodes all linked to one another. After retrieving this data we were able to input our current location and destination into the software, this would return the fastest route to a specific room. 
