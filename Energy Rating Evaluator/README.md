# Energy Rating Evaluator

[Product Walkthrough](https://greentrack.pplus.ai/)

[PLACEHOLDER for intro]

## How it works

[Video Walkthrough](https://drive.google.com/file/d/1T4iVqlRn78_FvFj4byGTDDc55B74qbyq/view)

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

## Demo Video

https://github.com/user-attachments/assets/e85a5398-0da3-423d-91f3-b079a51aec76

