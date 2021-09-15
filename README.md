## Let's count pixels
This is a test assignment for candidates for an online training at a well-known IT company.

This imaginary web service analyzes the image and counts pixels of black, white, and the color specified in the form (if any).

Image processing is performed in a horribly hackish manner without saving to the file system or database.

Extra features: target color masking and color comparison precision!

![Image](https://github.com/tconsta/pixelcount/blob/master/screenshot.jpg?raw=true)

## Run with docker:
```
git clone https://github.com/tconsta/pixelcount.git && \
cd pixelcount && \
docker-compose -f docker-compose.dev.yml up --build
```
and go to http://localhost:8000/