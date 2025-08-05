# LitWise Books - Book Recommendation System

A Python-based book recommendation system that discovers similar books based on user input. The system uses Open Library APIs to build a comprehensive book database and will later implement similarity matching based on book tags/labels derived from summaries and reviews.

## Features

- **Book Database**: Automatically populates a MySQL database with ~50 diverse books from Open Library
- **Cloud Database Support**: Works with popular cloud database providers
- **Rich Book Data**: Stores title, author, publication year, ISBN, subjects, descriptions, and more
- **Extensible Design**: Ready for future enhancement with recommendation algorithms

## Database Schema

The system stores books with the following fields:

- `id` - Primary key
- `title` - Book title
- `author` - Author name(s)
- `isbn` / `isbn13` - International Standard Book Numbers
- `first_publish_year` - Year of first publication
- `publisher` - Publisher name
- `number_of_pages` - Page count
- `openlibrary_key` - Open Library work identifier
- `description` - Book summary/description
- `subjects` - Comma-separated list of subjects/tags
- `average_rating` - Average rating (future enhancement)
- `rating_count` - Number of ratings (future enhancement)
- `language` - Book language
- `cover_image_url` - URL to book cover image
- `created_at` / `updated_at` - Timestamps

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Cloud Database

Choose one of the following cloud providers and create a MySQL database:

#### AWS RDS (Recommended)
1. Go to AWS RDS Console
2. Create a new MySQL database instance
3. Note the endpoint, port, username, and password

#### Google Cloud SQL
1. Go to Google Cloud Console
2. Create a new Cloud SQL MySQL instance
3. Note the public IP, username, and password

#### DigitalOcean Managed Database
1. Go to DigitalOcean Control Panel
2. Create a new Managed Database (MySQL)
3. Note the host, port, username, and password

#### PlanetScale (Serverless)
1. Sign up at planetscale.com
2. Create a new database
3. Get connection details from the dashboard

#### Railway (Simple Setup)
1. Go to railway.app
2. Deploy a MySQL database
3. Get connection details from the dashboard

### 3. Configure Environment

Create a `.env` file based on `env_template.txt`:

```bash
cp env_template.txt .env
```

Edit `.env` with your database credentials:

```env
DB_HOST=your-database-host.com
DB_PORT=3306
DB_NAME=litwise_books
DB_USER=your_username
DB_PASSWORD=your_password
```

### 4. Populate Database

Run the population script to fetch and store ~50 books:

```bash
python populate_books.py
```

This will:
- Create the database tables
- Fetch diverse books from Open Library API
- Store book data in your MySQL database
- Display progress and statistics

### 5. Verify Setup

Test your database connection:

```bash
python test_connection.py
```

## Project Structure

```
litwise-books/
├── requirements.txt          # Python dependencies
├── config.py                # Configuration management
├── models.py                # Database models (SQLAlchemy)
├── database.py              # Database connection utilities
├── openlibrary_client.py    # Open Library API client
├── populate_books.py        # Main script to populate database
├── test_connection.py       # Database connection test
├── env_template.txt         # Environment variables template
└── README.md               # This file
```

## API Usage

### Open Library Integration

The system uses Open Library's APIs:
- Search API: `https://openlibrary.org/search.json`
- Works API: `https://openlibrary.org/works/{id}.json`
- Covers API: `https://covers.openlibrary.org/b/id/{id}-L.jpg`

The client includes rate limiting and respectful API usage.

## Future Enhancements

1. **Recommendation Engine**: Implement similarity algorithms based on:
   - Book subjects/genres
   - Author similarity
   - Publication era
   - User ratings and reviews

2. **Tag Generation**: Use NLP to extract tags from:
   - Book descriptions
   - User reviews
   - Subject classifications

3. **Web Interface**: Build a web application for:
   - Book search and discovery
   - Recommendation requests
   - User preferences

4. **Review Integration**: Add support for:
   - Goodreads reviews
   - Amazon reviews
   - User-generated content

## Cloud Database Options Comparison

| Provider | Pros | Cons | Best For |
|----------|------|------|----------|
| AWS RDS | Highly reliable, scalable | More expensive | Production apps |
| Google Cloud SQL | Good integration with GCP | Complex pricing | Google ecosystem |
| DigitalOcean | Simple, predictable pricing | Limited features | Small to medium apps |
| PlanetScale | Serverless, branching | MySQL compatibility issues | Modern workflows |
| Railway | Very easy setup | Limited customization | Prototypes, demos |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

https://docs.google.com/document/d/1AvDKpvfwevwfjkFeacn5trUVuwSW_fAYUGHV7T547Fc/edit?usp=sharing
