from flask import Flask, render_template, jsonify
import requests
from collections import Counter

app = Flask(__name__)

# Fetch data from ThingSpeak for all 8 fields
def fetch_thingspeak_data(channel_id, read_api_key, results=10):
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results={results}"
    response = requests.get(url)
    data = response.json()
    feeds = data.get('feeds', [])
    return feeds

# Process clothing data and all other fields (e.g., field1 to field8)
def process_clothing_data(feeds):
    clothing_types = [feed['field1'] for feed in feeds if feed['field1']]
    clothing_counter = Counter(clothing_types)
    most_worn = clothing_counter.most_common(1)[0][0] if clothing_counter else "No data"

    # Fetch additional data from fields
    brand_names = [feed['field2'] for feed in feeds if feed['field2']]  # Clothing brand
    clothing_descriptions = [feed['field3'] for feed in feeds if feed['field3']]  # Clothing description/type
    wardrobe_temperature = [feed['field7'] for feed in feeds if feed['field7']]
    wardrobe_humidity = [feed['field8'] for feed in feeds if feed['field8']]

    # Determine most worn brand
    brand_counter = Counter(brand_names)
    most_worn_brand = brand_counter.most_common(1)[0][0] if brand_counter else "No brand data"

    # Least worn clothing
    least_worn = clothing_counter.most_common()[-1][0] if clothing_counter else "No data"

    # Last clothing item added
    last_item = feeds[-1] if feeds else {}

    return {
        "clothing_counts": clothing_counter,
        "most_worn": most_worn,
        "most_worn_brand": most_worn_brand,
        "least_worn": least_worn,
        "brand_names": brand_names,
        "clothing_descriptions": clothing_descriptions,
        "wardrobe_temperature": wardrobe_temperature,
        "wardrobe_humidity": wardrobe_humidity,
        "last_item": last_item
    }

# Route to fetch clothing and field data insights
@app.route('/insights')
def get_clothing_insights():
    # Fetch ThingSpeak data for clothing tracking and other fields
    channel_id = "2661669"  # Replace with your channel ID
    read_api_key = "0TVQRHJWDP1GBP3Y"  # Replace with your read API key
    feeds = fetch_thingspeak_data(channel_id, read_api_key)
    clothing_data = process_clothing_data(feeds)

    # Get clothing recommendations
    recommendations = "Based on your past usage, you should consider wearing your most frequently worn clothing item."

    return jsonify({
        "clothing_data": clothing_data,
        "recommendations": recommendations
    })

# Main route to render the insights page
@app.route('/')
def index():
    return render_template('insights.html')

if __name__ == "__main__":
    app.run(debug=True)
