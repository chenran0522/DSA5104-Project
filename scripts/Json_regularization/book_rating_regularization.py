import json

# File path


def normalize_book_ratings(file_path):
    try:
        # Load the JSON data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            books = json.load(file)

        # Normalize the 'rating' field by multiplying by 2
        for book in books:
            book["rating"] *= 2

        # Save the normalized data back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(books, file, ensure_ascii=False, indent=4)

        print("Ratings normalized successfully.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Use the function with the path to your JSON file
file_path = "../../data/json/book.json"
normalize_book_ratings(file_path)
