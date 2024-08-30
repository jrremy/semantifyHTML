def main():    
    from bs4 import BeautifulSoup

    html = """
    <html>
    <body>
        <div>
        <p>Hello, <b>world!</b></p>
        </div>
    </body>
    </html>
    """

    soup = BeautifulSoup(html, 'html.parser')

    # Iterate over all descendants of the <html> tag
    for descendant in soup.html.descendants:
        print(repr(descendant))
        
if __name__ == "__main__":
    main()