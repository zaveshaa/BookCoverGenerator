from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Tuple

#TODO:
# footnote of large titles
# change color of cover and font color


def create_book_cover(title: str, author: str, output_path: str, width: int = 600, height: int = 900, background_color: Tuple[int, int, int] = (255, 228, 196), title_color: Tuple[int, int, int] = (0, 0, 0), author_color: Tuple[int, int, int] = (0, 0, 0)) -> None:
    cover = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(cover)

    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        author_font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    title_x = (width - title_width) // 2
    title_y = (height - title_height) // 3

    draw.text((title_x, title_y), title, fill=title_color, font=title_font)

    author_bbox = draw.textbbox((0, 0), author, font=author_font)
    author_width, author_height = author_bbox[2] - author_bbox[0], author_bbox[3] - author_bbox[1]
    author_x = (width - author_width) // 2
    author_y = (height - author_height) * 2 // 3

    draw.text((author_x, author_y), author, fill=author_color, font=author_font)

    cover.save(output_path)

def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in " -_" else "_" for c in name)

def generate_covers_from_file(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    book_data: List[Tuple[str, str]] = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            title = lines[i]
            author = lines[i + 1]
            book_data.append((title, author))

    output_dir = os.path.join(os.path.dirname(file_path), "covers")
    os.makedirs(output_dir, exist_ok=True)

    for title, author in book_data:
        sanitized_title = sanitize_filename(title)
        output_path = os.path.join(output_dir, f"{sanitized_title}.png")
        create_book_cover(title, author, output_path)
        print(f"Created cover for '{title}' by {author} at {output_path}")

script_dir = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(script_dir, 'books.txt')
generate_covers_from_file(text_file_path)
