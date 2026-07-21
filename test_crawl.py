import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url2(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url3(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url4(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)


class Testget_heading_from_html(unittest.TestCase):
    def test_get_heading_from_html(self):
        input_html = """<html>
            <body>
                <h1>Welcome to Boot.dev</h1>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html2(self):
        input_html ="""<html>
            <body>
                <h2>Welcome to Boot.dev</h2>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_heading_from_html(input_html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html3(self):
        input_html = """<html>
            <body>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_heading_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html4(self):
        input_html = """<html>
            <body>
                <h3>Welcome to Boot.dev</h3>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_heading_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html5(self):
        input_html = """<html>
            <body>
                <h2>Welcome to Boot.dev</h2>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                <h1>Oooh baby</h1>
                </main>
            </body>
            </html>"""
        actual = get_heading_from_html(input_html)
        expected = "Oooh baby"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self) -> None:
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self) -> None:
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_whitespace(self) -> None:
        input_body = "<html><body><h1>   Whitespace Title   </h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Whitespace Title"
        self.assertEqual(actual, expected)
    

class Testget_paragraph_from_html(unittest.TestCase):
    def test_get_first_paragraph_from_html1(self):
        input_html = """<html>
            <body>
                <h1>Welcome to Boot.dev</h1>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html2(self):
        input_html ="""<html>
            <body>
                <h2>Welcome to Boot.dev</h2>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html3(self):
        input_html = """<html>
            <body>
                <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
                </main>
            </body>
            </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html4(self):
        input_html = """<html>
            <body>
                <h3>Welcome to Boot.dev</h3>
                <main>
                </main>
            </body>
            </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_no_paragraph(self) -> None:
        input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)



if __name__ == "__main__":
    unittest.main()