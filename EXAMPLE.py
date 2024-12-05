# Example usage
search_results = search_by_song("Shape of You")
for result in search_results:
    print(result.info())

search_results = search_by_singer("Ed Sheeran")
for result in search_results:
    print(result.info())
