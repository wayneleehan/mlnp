## Project Structure

```text
├── README.md
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── models
│   │   ├── routers
│   │   │   └── stock.py
│   │   ├── schemas
│   │   │   └── stock.py
│   │   └── services
│   │       ├── ai_service.py
│   │       ├── news_service.py
│   │       └── stock_service.py
│   ├── requirements.txt
│   ├── scripts
│   │   └── init_stock_list.py
│   └── stocks.db
└── frontend
    ├── eslint.config.js
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── public
    │   └── vite.svg
    ├── src
    │   ├── App.css
    │   ├── App.jsx
    │   ├── assets
    │   │   └── react.svg
    │   ├── components
    │   │   ├── SearchBar.css
    │   │   └── SearchBar.jsx
    │   ├── index.css
    │   └── main.jsx
    └── vite.config.js


