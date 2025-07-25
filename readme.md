## Problem

Jobs with lineage/ dependency graph as follows (we are assuming non cyclicality b/c of the nature of data pipelines, one stage of the data pipeline cannot be the source of it's source) : 

height

    3     Z            B       Q*   X
           \        /   \       \ / |    
    2        C      D      E     Q  |        
           /  \   /  \    / \  /    |  
    1      AA   AB    AC AD  AE     | 
           \  /       \ /   /       |
    0      --- GLOBAL SOURCE TABLES ---

                        


| Job ID | Output Table | Source Tables | 
| ---  | --- | ---  | 
| 1 | Z | [C] |
| 2 | B | [D,E] |
| 3 | C | [AA,AB] |
| 4 | D | [AB,AC] |
| 5 | E | [AD,AE] |
| 6 | AA | [SOURCE TABLES] |
| 7 | AB | [SOURCE TABLES] |
| 8 | AC | [SOURCE TABLES] |
| 9 | AD | [SOURCE TABLES] |
| 10 | AE | [SOURCE TABLES] |
| 11 | Q | [AE] |
| 12 | Q* | [Q] |
| 13 | X | [Q, SOURCE TABLES]



## Similarity Analysis  

#### With respect to the similarities between two nodes, there has to be the following considerations:
1. Each node/job has shared connections based on its source tables
2. Two Jobs that share direct source tables are similar to another
    - Node C and Node D are similar to each other because they share the same (direct) source tables
3.  Two jobs that share a data lineage (indirect source tables) are also similar to each other
    - On the example tree, job #1 (Output Table Z) is more siliar to job #2 (Output Table B) **than** it is to job #11 (Output Table Q) EVEN though Z [C] shares no DIRECT source tables with B [D,E] because Z & B share AB in common
4. However, the more distant (more levels of distance from each other) the jobs' source tables are, the less similar they are
    - For an example:
        - let's say a ML team's data pipeline consists of the following jobs: Global Source -> ML Aggregation -> ML Transformation --> Feature DataSet
        - An analytics team's data pipeline consists of the following jobs: Global Source -> AL Aggregation -> AL Transformation --> Visualization & Query Platform
        - Here, the AL Transformation step and the ML Transformation step are similar, because they share the same direct source table.         
        - ML Transformation and AL Transformation are still related, but are much less so due to the fact that their shared lineage is more distant (at the Global Source)
        - Lets suggest that the ML Aggregation is a median func, 
        - Let suggest thatt he AL  Aggregation is a mean func
        - The meadian and mean functions are working on the same dataset but generating different statistics, and it would be reasonable to suggest that the two functions are very similar
        - By the time we get to the ML Transformation and AL Transformatoin jobs however, they are working on very different data, although they both share a common data heritage in the global source tables. 
5. In order to account for #4, we have to weigh more distance shared source tables less than shared source tables that are closer in distance. 
    - Most > linear function to generate the weights should work, but I'll go with an inverse exponential function to weigh the similarity scores of different distance similarities
## Similarity Function 
$$Similarity = \sum_{n=1}^{min(A.height,\space \space B.height)}1/2^{(x-n)}*(A.source\space tables\space at \space n \cap B.source\space tables\space at \space n )$$
Where $$height = Distance/Steps \space from \space Global \space  Source \space Tables$$
and  $$x = max(A.height,\space \space B.height)$$

### Reasoning
- We want to calculate similiarty based on the number of shared identical source tables
- Source tables further away (multiple levels of dependencies away from the nodes) should be weighted less
- The Weight func   
     $$1/2^{(x-n)}$$ 
     faciliates the weight function rewards closeness of the common source tables and reduces the common source tables more distant

- We use this summation b/c we want to go from 1 (the function assumes that source stables are shared by all nodes in graph) to the min height of the two nodes that we are comparing because at n = min_neight + 1, there will be no more shared source tables
$$ \sum_{n=1}^{min(A.height,\space \space B.height)} $$

## Plan
In order to facilitate this similarity function, I'll do the following:
1. Put jobs as nodes in the tree, edges are source table dependencies
2. During the tree injection process, the node/job should also be assigned the height or the distance from global source tables
3. When two nodes are compared, we get the min height and start working our way down (from min height) calcuating the number of the intersection set between the source tables 
4. Weigh the sum of level n by the weight func
5. Return the weighted sum of all levels
6. ...
7. Profit???


## Instructions
Please use the unittest file tests/test_node.py as a template for how to start this lineage tree 

Recommend python >= 3.13
No libraries outside default python libs were used

>>> python3 -m unittest tests/test_tree.py