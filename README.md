# Kentavr Movie Bot

A modular and robust Telegram bot built with **Aiogram 3** that allows users to search for movies, view detailed descriptions, check popular movies, and manage their personal movie history and favorites. The project fetches real-time data using the **The Movie Database (TMDb) API**.

---

## 🚀 Features

* **Real-time Movie Search:** Search for any movie by its title via the TMDb API.
* **Rich Movie Details:** Displays movie titles, release years, genres, ratings, and overviews along with posters.
* **Popular Movies:** Quick access to currently trending and popular movies.
* **User History:** Automatically tracks and displays user search history using a local JSON-based storage.
* **Favorites System:** Users can add movies to their favorites list for quick access later.

---

## 🛠️ Architecture & Tech Stack

The project follows a clean **Modular Architecture**, strictly separating the presentation layer (frontend/handlers) from the data layer (backend/services).

* **Language:** Python 3.11+
* **Framework:** [Aiogram 3.x](https://github.com/aiogram/aiogram) (Asynchronous Telegram Bot API)
* **API Client:** [Aiohttp](https://github.com/aio-libs/aiohttp) (Asynchronous HTTP Requests)
* **Database/Storage:** Local JSON File Storage (`services/storage.py`)
* **Environment Management:** `python-dotenv`

### Project Structure

```text
├── data/
│   ├── history.json          # Stores users' search history
│   └── favorites.json        # Stores users' favorite movies
├── handlers/
│   ├── __init__.py
│   └── client.py             # UI Handlers (commands, buttons, search)
├── services/
│   ├── __init__.py
│   ├── movie_api.py          # TMDb API integration & OOP Data Models
│   └── storage.py            # Local JSON storage logic
├── .env                      # Environment variables (Tokens & Keys)
├── config.py                 # Configuration loader
├── main.py                   # Bot entry point
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
