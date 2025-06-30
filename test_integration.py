import requests

base_url = "http://localhost:8000"

def test_homepage():
    res = requests.get(f"{base_url}/")
    assert res.status_code == 200

def test_article_post():
    res = requests.post(f"{base_url}/articles/", json={"content": "This is a test article."})
    assert res.status_code == 200
    assert "label" in res.json()

def test_url_post():
    res = requests.post(f"{base_url}/articles/from_url/", json={"url": "https://www.bbc.com/news"})
    assert res.status_code in [200, 400]

def test_get_articles():
    res = requests.get(f"{base_url}/articles/")
    assert res.status_code == 200

if __name__ == "__main__":
    try:
        test_homepage()
        print("Homepage test passed")
        test_article_post()
        print("Article POST test passed")
        test_url_post()
        print("URL POST test passed")
        test_get_articles()
        print("GET articles test passed")
    except AssertionError as e:
        print("A test failed:", e)
