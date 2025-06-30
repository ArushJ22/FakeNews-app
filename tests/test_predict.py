import pytest
from main import predict_label

def test_normal_text():
    text = "This is a real news article about elections."
    label = predict_label(text)
    assert label in ["real", "fake"]

def test_empty_input():
    text = ""
    label = predict_label(text)
    assert label in ["real", "fake"]

def test_long_text():
    text = "This is a very long news article. " * 200
    label = predict_label(text)
    assert label in ["real", "fake"]

def test_random_symbols():
    text = "@#$%^&*()"
    label = predict_label(text)
    assert label in ["real", "fake"]
