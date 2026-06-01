import os
import pytest
from blackjack import (
    HIGHSCORE_FILE, create_deck, card_value, hand_value, is_soft,
    SUITS, RANKS, load_scores, save_score
)

# -------------------------------
# DECK TESTS
# -------------------------------

def test_create_deck_size():
    deck = create_deck()
    assert len(deck) == 52

def test_create_deck_unique_cards():
    deck = create_deck()
    assert len(deck) == len(set(deck))  # no duplicates

def test_deck_contains_valid_cards():
    deck = create_deck()
    for rank, suit in deck:
        assert rank in RANKS
        assert suit in SUITS

# -------------------------------
# CARD VALUE TESTS
# -------------------------------

def test_card_value_number():
    assert card_value(("5", "♠")) == 5

def test_card_value_face_cards():
    assert card_value(("J", "♣")) == 10
    assert card_value(("Q", "♦")) == 10
    assert card_value(("K", "♥")) == 10

def test_card_value_ace():
    assert card_value(("A", "♠")) == 11
    
# -------------------------------
# HAND VALUE TESTS
# -------------------------------

def test_hand_value_no_aces():
    hand = [("10", "♠"), ("9", "♥")]
    assert hand_value(hand) == 19
def test_hand_value_single_ace_soft():
    hand = [("A", "♣"), ("6", "♦")]
    assert hand_value(hand) == 17

def test_hand_value_single_ace_hard():
    hand = [("A", "♣"), ("9", "♦"), ("8", "♠")]
    assert hand_value(hand) == 18  # Ace becomes 1

def test_hand_value_multiple_aces():
    hand = [("A", "♣"), ("A", "♦"), ("9", "♠")]
    assert hand_value(hand) == 21  # 11 + 1 + 9

def test_is_soft_true():
    hand = [("A", "♣"), ("5", "♦")]
    assert is_soft(hand) is True

def test_is_soft_false():
    hand = [("A", "♣"), ("9", "♦"), ("8", "♠")]
    assert is_soft(hand) is False  # hard hand

# -------------------------------
# HIGHSCORE TESTS
# -------------------------------

@pytest.fixture
def clean_highscore_file():
    """Ensures highscores file starts empty."""
    if os.path.exists(HIGHSCORE_FILE):
        os.remove(HIGHSCORE_FILE)
    yield
    if os.path.exists(HIGHSCORE_FILE):
        os.remove(HIGHSCORE_FILE)

def test_load_scores_empty(clean_highscore_file: None):
    scores = load_scores()
    assert scores["Easy"] == []
    assert scores["Medium"] == []
    assert scores["Hard"] == []

def test_save_and_load_scores(clean_highscore_file: None):
    save_score("Easy", "Alice", 120)
    save_score("Easy", "Bob", 90)

    scores = load_scores()
    assert len(scores["Easy"]) == 2
    assert scores["Easy"][0]["name"] == "Alice"
    assert scores["Easy"][0]["score"] == 120

def test_highscore_limit(clean_highscore_file: None):
    # Add 7 scores, only top 5 should remain
    for i in range(7):
        save_score("Medium", f"Player{i}", i * 10)

    scores = load_scores()
    assert len(scores["Medium"]) == 5
    assert scores["Medium"][0]["score"] == 60  # highest
    assert scores["Medium"][-1]["score"] == 20  # lowest of top 5
