# Green Building Copilot
AI tool that would help automating some tasks in the certification of green buildings. 

1. We aim to essentially use AI to validate and verify various checklists within the [GRIHA Standards](https://www.grihaindia.org/files/Manual_VolI.pdf)
2. One parameter within the standards (10% weightage) that is termed sustainable site planning is what this tool aims to validate


## The problem 

We are building this to solve the following problems

* Green building certification is a process that requires lots of human efforts 
* This is also a lengthy process
* And an expensive process

This leads to less adoption of Green Buildings

## The solution  

Imagine an AI copilot tool that would help various stakeholders in the green building certification process (builders, consultants, green building standard body, ULBs) quickly and efficiently verify compliance with GRIHA standards and claim the benefits

## How does this work ?

- This is a [worksheet](https://docs.google.com/spreadsheets/d/1ACInZjybHO91J53p1HrEaPxn8wKxdPAppkET2UgFlZw/edit?usp=sharing) that contains all the GRIHA parameters that need to validated once relevant documents are uploaded.
- We did some priliminary assessment of the feasibility of which parameters can be automated. Some of the document required for automation has also been identified and provided in the worksheet.

Here are some of the key steps we can get started with

1. Builders/consultants will upload the necessary documents including photos, videos, invoices, site plans...etc 
2. Extract location details either from the files uploaded using OCR or directly upload the coordinates 
3. Detect old trees, minimum nos of trees,...etc in the site plan using vision AI
5. Use google map API or any OSM to say whether public facilities and amenities are present within the threshold
7. Use computer vision to analyse designated vehicular tracks for NMT vehicles 


## Next Commitments

We are looking for enthusiastic volunteers who can own pieces of this design puzzle. Please reach out to meghana@peopleplus.ai/vishnu@peopleplus.ai if you have expertise and/or interest in:

1. **Technical Architecture**: Build out this capabilities using machine learning.


## Questions?

If you have any queries/doubts or new ideas regarding this project please create an issue in this repo. Let's have a discussion! For any other queries, please reach out to [meghana](mailto:meghana@peopleplus.ai) 


Learn more about other [people+ai](https://peopleplus.ai/) initiatives.
