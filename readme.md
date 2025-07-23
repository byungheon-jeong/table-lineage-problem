## Problem

Jobs with lineage/ dependency graph as follows: 

                            
         Z            B           Q*
           \        /   \        /
            C      D      E     Q    
           /  \   /  \    / \  /
          AA   AB    AC AD  AE
           \  /       \ /   /
        --- GLOBAL SOURCE TABLES ---

                        


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
    #### Similarity = 
    $$\sum_{n=0}^{max(A.height,\space \space B.height) - 1}1/2^n*(\#Shared\space common\space tables\space at \space level \space n)$$

