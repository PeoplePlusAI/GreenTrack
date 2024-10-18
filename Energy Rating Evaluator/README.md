# Energy Rating Evaluator

This tool automates the verification of energy efficency compliance under green building rating systems. Under **Green Rating for Integrated Habitat Assessment (GRIHA)** guidelines, all electrical equipments used in the building must be Bureau of Energy Efficency (BEE) star rated. Only if the equipment is rated 3 star or above will it be considered GRIHA compliant. This tool fetches the BEE star rating of any given electrical appliance to assess GRIHA compliance. Use the link below to test it out :-

[Product Walkthrough](https://greentrack.pplus.ai/)

## How it works

https://github.com/user-attachments/assets/e85a5398-0da3-423d-91f3-b079a51aec76

## Getting Started

Rename [`.env.example`](.env.example) to `.env`:
```
mv .env.example .env
```
Make any necessary changes to the fields.

## Run service (Docker)

To start the backend, run:
```
docker compose up -d --build
```

Visit [http://localhost:6001](http://localhost:6001) to view the frontend.

## Run service (Podman)

Build the container:
```
podman build -t scraper-backend .
```

Run the container:
```
podman run -d \
  --name scraper \
  --env-file .env \
  -p 6001:6001 \
  scraper-backend \
  python3 manage.py runserver 0.0.0.0:6001
```



