import pytest
from tracks_library import LibraryItem

class TestLibraryItem:
    
    def test_library_item_initialization(self):
        """Test successful initialization of LibraryItem."""
        item = LibraryItem("Shape of You", "Ed Sheeran", 5, "http://example.com")
        assert item.title == "Shape of You"
        assert item.singer == "Ed Sheeran"
        assert item.rating == 5
        assert item.link == "http://example.com"
        assert item.play_count == 0  # Default play count should be 0

    def test_info_method(self):
        """Test the info method of LibraryItem."""
        item = LibraryItem("Shape of You", "Ed Sheeran", 5, "http://example.com", play_count=10)
        expected_info = ("Shape of You", "Ed Sheeran", 5, 10)
        assert item.info() == expected_info

    def test_invalid_rating_string(self):
        """Test that a ValueError is raised for non-integer rating."""
        with pytest.raises(ValueError, match="Rating must be an integer between 0 and 5."):
            LibraryItem("Invalid Song", "Artist", 'four', "http://example.com")

    def test_invalid_rating_out_of_bounds(self):
        """Test that a ValueError is raised for out-of-bounds rating."""
        with pytest.raises(ValueError, match="Rating must be an integer between 0 and 5."):
            LibraryItem("Invalid Song", "Artist", 6, "http://example.com")

    def test_invalid_play_count_negative(self):
        """Test that a ValueError is raised for negative play count."""
        with pytest.raises(ValueError, match="Play count must be a non-negative integer."):
            LibraryItem("Invalid Song", "Artist", 4, "http://example.com", play_count=-1)

    def test_invalid_play_count_string(self):
        """Test that a ValueError is raised for non-integer play count."""
        with pytest.raises(ValueError, match="Play count must be a non-negative integer."):
            LibraryItem("Invalid Song", "Artist", 4, "http://example.com", play_count='ten')

if __name__ == '__main__':
    pytest.main()