import instaloader
import json

# Create an instance of Instaloader
loader = instaloader.Instaloader()

# List of post URLs
post_urls = [
    "https://www.instagram.com/p/CMf-caUAQht/",
    "https://www.instagram.com/p/ClhLem0s01f/",
    "https://www.instagram.com/p/CpgInkDyUlj/",
    "https://www.instagram.com/p/CtKfI6mOsN0/",
    "https://www.instagram.com/p/CbqAcdSsdaN/",
    "https://www.instagram.com/p/CsC0YWKhDhv/",
    "https://www.instagram.com/p/CMSj-QLhd0R/",
    "https://www.instagram.com/p/Co_8qxeNBIB/",
    "https://www.instagram.com/p/ChZiarYM4Nj/",
    "https://www.instagram.com/p/CtvD_5YMRHu/"
]

# Prepare a list to store the JSON results
results = []

# Iterate over the post URLs
for post_url in post_urls:
    # Load the post using its URL
    post = instaloader.Post.from_shortcode(loader.context, post_url.split("/")[-2])

    # Extract the desired information
    caption = post.caption.encode('ascii', 'ignore').decode('ascii')  # Remove non-ASCII characters from the caption
    hashtags = [f"#{tag}" for tag in post.caption_hashtags]
    #image_location = ''
    post_id = post_url.split('/')[-2]
    # Prepare the JSON result for the current post
    result = {
        "Post_id": post_id,
        "caption": caption,
        "hashtags": hashtags,
        #"image_location": image_location
    }

    # Append the JSON result to the list
    results.append(result)

# Save the JSON results to a file
with open("result.json", "w") as file:
    json.dump(results, file, indent=2)

print("JSON file 'result.json' has been created.")
