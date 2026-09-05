
def supernova_malayalam_translator(input_text):
    import http.client
    import json
    import unicodedata

    conn = http.client.HTTPSConnection("getsupernova.ai")

    # Create the JSON payload.
    payload = json.dumps({
        "id": "zl0aal1XIXXS3QEx",
        "original_text": input_text,
        "language": "Malayalam"
    })

    # Define the headers.
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://getsupernova.ai',
        'referer': 'https://getsupernova.ai/translate/english-to-malayalam',
    }

    # Send the POST request.
    conn.request("POST", "/api/chat-translate", payload, headers)
    res = conn.getresponse()

    # Read the full response.
    # If the API streams the response, it's read as one byte stream.
    data = res.read().decode("utf-8")
    conn.close()

    lines = data.splitlines()

    # Extract the actual text from each line.
    chunks = []
    for line in lines:
        if ":" in line:
            # Split on the first colon and remove quotes and extra spaces.
            parts = line.split(":", 1)
            text_chunk = parts[1].strip().strip('"')
            chunks.append(text_chunk)
        else:
            chunks.append(line.strip())

    # Concatenate all text chunks.
    combined_text = "".join(chunks)

    # Normalize the text to NFC form to ensure proper Malayalam ligatures.
    normalized_text = unicodedata.normalize('NFC', combined_text)

    return normalized_text
