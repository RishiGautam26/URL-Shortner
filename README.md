# URL Shortener Microservice 🔗

A FastAPI-based URL shortening service with click tracking and custom alias support.

## Features ✨
- **URL Shortening**: Convert long URLs to short codes
- **Custom Aliases**: Optionally specify your own short code
- **Click Tracking**: Monitor how many times each link is clicked
- **Duplicate Prevention**: Automatic reuse of existing short codes for duplicate URLs
- **CORS Enabled**: Ready for web app integration
- **Lightweight**: SQLite backend with minimal dependencies

## Installation 💻

1. **Requirements**:
   - Python 3.7+
   - Required packages:
     ```
     pip install fastapi uvicorn pydantic python-multipart
     ```

2. **Run the server**:
```bash
uvicorn main:app --reload
```


## API Reference 📚

### Shorten URL `POST /shorten`
**Request**:

```Response
{
"long_url": "https://your-long-url.com"
}
```


**Parameters**:
- `alias` (optional query parameter): Custom short code

**Response**:

```Response
{
"short_url": "http://127.0.0.1:8000/abc123"
}
```


### Redirect `GET /{short_code}`
- 302 redirect to original URL
- Automatically increments click counter

### Get Statistics `GET /stats/{short_code}`
**Response**:

```Response
{
"long_url": "https://original-url.com",
"clicks": 42
}
```


## Example Usage 🚀

1. **Create short URL**:

```bash
curl -X POST "http://localhost:8000/shorten?alias=perplex"
-H "Content-Type: application/json"
-d '{"long_url": "https://www.perplexity.ai"}'
```


2. **Use custom alias**:

```bash
curl -X POST "http://localhost:8000/shorten?alias=myalias"
-H "Content-Type: application/json"
-d '{"long_url": "https://example.com"}'
```


3. **Get stats**:

```bash
curl http://localhost:8000/stats/perplex
```


## Configuration ⚙️
- **CORS**: Pre-configured to allow all origins
- **Database**: Automatically creates `urls.db` SQLite file
- **Short Code**:
- Default length: 6 characters
- Character set: A-Z, a-z, 0-9

## Contributing 🤝
1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push branch (`git push origin feature/improvement`)
5. Open Pull Request

## License 📄
MIT License - free for personal and commercial use



























