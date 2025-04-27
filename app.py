"""
This is a simple app setup script created with `render-engine init`
"""

from render_engine import (
    Site,
    Page,
    Collection,
    Blog
)
from render_engine_markdown import MarkdownPageParser

app = Site()
app.output_path = "build"

app.site_vars.update({
    "SITE_TITLE":"Jamal Hansen",
    "SITE_URL":"http://jamalhansen.com",
    "NAVIGATION":[
        {
            "name": "Home",
            "url": "/",
        },
        {
            "name": "Collection Page",
            "url": "/example-page.html",
        },
        {
            "name": "Blog",
            "url": "/blog/blog.html",
        },
    ]
    })

@app.page
class Index(Page):
    template = "index.html"

@app.collection
class Pages(Collection):
    content_path = "content/pages" # path to content files
    routes = ["./"] # route to collection page
    template = "page.html"

@app.collection
class Blog(Blog):
    content_path = "content/blog" # path to content files
    routes = ["blog"] # route to collection page
    pageParser = MarkdownPageParser
    template = "page.html"

if __name__ == "__main__":
    app.render()
