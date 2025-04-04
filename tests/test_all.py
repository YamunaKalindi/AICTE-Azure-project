from src.main import main

def test_basic():
    main("Find top 5 AI headlines and save to file")
    with open("ai_headlines.txt", "r") as f:
        assert len(f.readlines()) == 5
    print("Basic test passed!")

if __name__ == "__main__":
    test_basic()