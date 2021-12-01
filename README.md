# CSCI596_final_proj
Ming Wang, Zhengxie Hu

## 1.Introduction
The goal of our project is to use Directed MPNN (D-MPNN) to predict molecular property which will accelerate the development of new chemical product. 

## 2.Dataset
- We used scraped data from PoLyInfo database by Japan National Institute for Materials Science.
- We extracted the rheological property (melt viscosity) and electrical property (dielectric dispersion) and use it as input to the D-MPNN. 
![image](polyinfo_result.png)

## 3.Objective
- Apply D-MPNN to this new dataset to predict some property of polymers.
paper link: [https://pubs.acs.org/doi/10.1021/acs.jcim.9b00237](https://pubs.acs.org/doi/10.1021/acs.jcim.9b00237)
![D-MPNN](D-MPNN.jpeg)

- Visualize the result via t-SNE to reveal some relationships between polymers.
