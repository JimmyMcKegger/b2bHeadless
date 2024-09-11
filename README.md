# Customer Accounts FastAPI Application

This project is a FastAPI application that integrates with Shopify's Customer Accounts API with a confidential client. Follow the instructions below to clone the repository, install dependencies, and run the application.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Ngrok](https://ngrok.com/download)
- Shopify store with a Hydrogen or Headless sales channel and a Confdential client

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/JimmyMckegger/customerAccounts.git
cd customerAccounts
```

### 2. Install Dependencies
```
poetry install
```

### 3. Start Ngrok

```bash
ngrok http 8000
```

### 4. Set Environment Variables

Replace th values in the `.env.example` file and rename the file to `.env`

```env
SHOP_ID=123123123
CLIENT_ID=shp_asdf234asdf123sadf123
CLIENT_SECRET=3c50fsadfkljhsadfkljhasdfkjhd
DOMAIN=your-ngrok-domain.ngrok-free.app
```

### 5. Run the Application

```bash
poetry shell && uvicorn main:app --reload
```

