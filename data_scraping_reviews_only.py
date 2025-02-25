input_file = "apex_legends_english_reviews.txt"
output_file = "apex_legends_reviews_only.txt"

with open(input_file, "r", encoding="utf-8") as infile:
    content = infile.read()
    
    # Split by double newline to get each review block
    review_blocks = content.split("\n\n")
    
    # Extract only the review text from each block
    reviews_only = []
    for block in review_blocks:
        if not block.strip():
            continue
        
        # Find where the review text starts (after "Review: ")
        lines = block.split("\n")
        for line in lines:
            if line.startswith("Review: "):
                review_text = line[8:]
                reviews_only.append(review_text)
                break

with open(output_file, "w", encoding="utf-8") as outfile:
    for review in reviews_only:
        outfile.write(f"{review}\n\n")

print(f"Successfully extracted {len(reviews_only)} reviews to {output_file}")