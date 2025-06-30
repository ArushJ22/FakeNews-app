from main import predict_label

def run_edge_tests():
    edge_cases = [
        "",  # Empty input
        "🔥",  # Emoji
        "a",  # One character
        "Breaking News!",  # Vague
        "Government launches new education policy to improve standards.",  # Real-like
        "Aliens invaded Earth and no one noticed.",  # Fake-like
        "COVID-19 vaccines turn people into lizards.",  # Obvious fake
        "The price of oil surged due to market volatility." * 50  # Long text
    ]
    
    for i, case in enumerate(edge_cases):
        try:
            label = predict_label(case)
            print(f"[{i+1}] Input: {case[:60]}... → Prediction: {label}")
        except Exception as e:
            print(f"[{i+1}] Input caused error: {e}")

if __name__ == "__main__":
    run_edge_tests()
