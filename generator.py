import pandas as pd
import random

# Categories and their specific attributes for realistic tags
data_map = {
    "Electronics": (["Laptop", "Smartphone", "Smartwatch", "Tablet", "Camera"], ["Pro", "Ultra", "Lite", "Max"], ["4k", "fast-charging", "oled", "portable", "waterproof"]),
    "Audio": (["Headphones", "Speaker", "Earbuds", "Soundbar"], ["Sonic", "Echo", "Alpha", "Pure"], ["bluetooth", "noise-cancelling", "wireless", "bass", "hi-fi"]),
    "Furniture": (["Chair", "Desk", "Sofa", "Lamp", "Shelf"], ["Ergo", "Zenith", "Modern", "Minimal"], ["wood", "office", "comfortable", "metal", "adjustable"]),
    "Peripherals": (["Keyboard", "Mouse", "Webcam", "Mic"], ["Mechanical", "Gaming", "Aero", "Pro"], ["rgb", "tactile", "wireless", "optical", "streaming"])
}

products = []
img_placeholders = [
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30", # Watch
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", # Headphone
    "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf", # Monitor
    "https://images.unsplash.com/photo-1542491595-62e924f3365a"  # Clock
]

for i in range(1, 1001):
    cat = random.choice(list(data_map.keys()))
    items, brands, tags = data_map[cat]
    
    name = f"{random.choice(brands)} {random.choice(items)} {random.randint(100, 999)}"
    price = random.randint(20, 1500)
    img = random.choice(img_placeholders)
    desc = f"A premium {name} designed for {cat} enthusiasts."
    product_tags = f"{cat.lower()} {random.sample(tags, 3)[0]} {random.sample(tags, 3)[1]} gear"
    
    products.append([i, name, cat, price, img, desc, product_tags])

df = pd.DataFrame(products, columns=['id', 'name', 'category', 'price', 'image_url', 'description', 'tags'])
df.to_csv("products.csv", index=False)
print("✅ products.csv generated with 1000 items!")