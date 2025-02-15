from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

# HTML Template for Input Form
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VISHANU XD TOK3NðŸ˜ˆ</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        input[type="text"] { width: 100%; max-width: 400px; padding: 8px; margin-top: 10px; }
        button { padding: 10px 20px; margin-top: 10px; background: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 10px; background: #f4f4f4; border: 1px solid #ddd; }
        .error { color: red; }
        .output-box { 
            width: 100%; 
            max-width: 400px; 
            padding: 10px; 
            margin-top: 10px; 
            background: #fff; 
            border: 1px solid #ccc; 
            font-family: monospace; 
        }
        .copy-button { 
            padding: 8px 16px; 
            margin-top: 10px; 
            background: #28a745; 
            color: white; 
            border: none; 
            cursor: pointer; 
        }
        .copy-button:hover { background: #218838; }
        .clear-button { 
            padding: 8px 16px; 
            margin-top: 10px; 
            background: #dc3545; 
            color: white; 
            border: none; 
            cursor: pointer; 
        }
        .clear-button:hover { background: #c82333; }
        .loading-spinner { 
            display: none; 
            margin-top: 10px; 
            border: 4px solid #f3f3f3; 
            border-top: 4px solid #007BFF; 
            border-radius: 50%; 
            width: 30px; 
            height: 30px; 
            animation: spin 1s linear infinite; 
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    <script>
        function copyToClipboard() {
            const outputBox = document.getElementById("output-box");
            outputBox.select();
            document.execCommand("copy");
            alert("Copied to clipboard!");
        }

        function clearForm() {
            document.getElementById("facebook_access_token").value = "";
            document.getElementById("output-box").value = "";
            document.getElementById("result").style.display = "none";
        }

        function showLoading() {
            document.getElementById("loading-spinner").style.display = "block";
        }
    </script>
</head>
<body>
    <h1>G3T INSTAGRAM TOK3N:</h1>
    <form action="/get-instagram-token" method="POST" onsubmit="showLoading()">
        <label for="facebook_access_token">ENT3R YOUR FACEBOOK ID TOK3N:</label><br>
        <input type="text" id="facebook_access_token" name="facebook_access_token" required><br><br>
        <button type="submit">G3T INSTAGRAM TOK3N:</button>
        <button type="button" class="clear-button" onclick="clearForm()">Clear Form</button>
    </form>

    <div id="loading-spinner" class="loading-spinner"></div>

    {% if instagram_token %}
        <div class="result" id="result">
            <p><strong>INSTAGRAM TOK3N:</strong></p>
            <input type="text" id="output-box" class="output-box" value="{{ instagram_token }}" readonly>
            <button class="copy-button" onclick="copyToClipboard()">Copy to Clipboard</button>
            {% if expiry_date %}
                <p><strong>Expiry Date:</strong> {{ expiry_date }}</p>
            {% endif %}
        </div>
    {% endif %}

    {% if error %}
        <div class="error">
            <p><strong>Error:</strong> {{ error }}</p>
        </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    # Render the form for GET requests
    return render_template_string(INDEX_HTML)

@app.route('/get-instagram-token', methods=['POST'])
def get_instagram_token():
    try:
        # Get the Facebook access token from the form
        facebook_access_token = request.form.get('facebook_access_token')

        if not facebook_access_token:
            return render_template_string(INDEX_HTML, error='Facebook access token is required')

        # Step 1: Verify the token and check if it has Instagram permissions
        verify_url = f'https://graph.facebook.com/v18.0/me?access_token={facebook_access_token}'
        verify_response = requests.get(verify_url)
        verify_data = verify_response.json()

        if 'error' in verify_data:
            return render_template_string(INDEX_HTML, error=verify_data['error']['message'])

        # Step 2: Use the Facebook access token as the Instagram token
        instagram_token = facebook_access_token

        # Step 3: Get token expiry date (if available)
        debug_token_url = f'https://graph.facebook.com/v18.0/debug_token?input_token={facebook_access_token}&access_token={facebook_access_token}'
        debug_response = requests.get(debug_token_url)
        debug_data = debug_response.json()

        expiry_date = None
        if 'data' in debug_data and 'expires_at' in debug_data['data']:
            expiry_timestamp = debug_data['data']['expires_at']
            expiry_date = datetime.fromtimestamp(expiry_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Render the result
        return render_template_string(INDEX_HTML, instagram_token=instagram_token, expiry_date=expiry_date)

    except Exception as e:
        return render_template_string(INDEX_HTML, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
