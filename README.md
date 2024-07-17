# Green Building Copilot
This is an AI tool that would help automate the process of green building certification. 

1. We aim to use AI to validate and verify various parameters within the [GRIHA Standards](https://www.grihaindia.org/files/Manual_VolI.pdf)
2. We aim to demo the tool by automating the verification of one parameter within the standard (10% weightage), termed sustainable site planning.

## The problem 

The green building certification process is: 

* Lengthy
* Expensive
* High in human effort

This leads to lesser adoption of green buildings. Our aim is to solve these challenges and incentivise green buildings using AI. 

## The solution  

Imagine an AI tool that would help various stakeholders in the green building certification process (builders, consultants, green building certification body, ULBs) quickly and efficiently verify compliance with GRIHA standards and claim the benefits. 

![](https://github.com/PeoplePlusAI/Green-Building-Copilot/assets/149042870/100a6844-53f5-4046-9024-7a8de5e6e59e=25x25)


## How does this work ?

- This is a [worksheet](https://docs.google.com/spreadsheets/d/1ACInZjybHO91J53p1HrEaPxn8wKxdPAppkET2UgFlZw/edit?usp=sharing) that contains all the GRIHA parameters that need to validated once relevant documents are uploaded.
- We did some priliminary assessment of the feasibility of which parameters can be automated. Some of the document required for automation has also been identified and provided in the worksheet.

Here are some of the key steps we can get started with:
1. Builders/consultants will upload the necessary documents including photos, videos, invoices, site plans...etc 
2. Extract location details either from the files uploaded using OCR or directly upload the coordinates 
3. Detect old trees, minimum nos of trees,...etc in the site plan using vision AI
5. Use google map API or any OSM to say whether public facilities and amenities are present within the threshold
7. Use computer vision to analyse designated vehicular tracks for NMT vehicles 

## Next Commitments

We are looking for enthusiastic volunteers who can own pieces of this design puzzle. Please reach out to meghana@peopleplus.ai/vishnu@peopleplus.ai if you have expertise and/or interest in:

1. **Technical Architecture**: Build out these capabilities using machine learning.


## Questions?

If you have any queries/doubts or new ideas regarding this project please create an issue in this repo. Let's have a discussion! For any other queries, please reach out to [meghana](mailto:meghana@peopleplus.ai) 


Learn more about other [people+ai](https://peopleplus.ai/) initiatives.

## Setup

Rename [`.env.example`](.env.example) to `.env`:
```
mv .env.example .env
```
Make any necessary changes to the fields.

Then,  to start the backend, run:
```
docker compose up -d --build
```

Visit [http://localhost:6001](http://localhost:6001) to view the frontend.
