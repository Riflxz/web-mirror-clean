import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from urllib.parse import urlparse, urljoin
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from content_cleaner import ContentCleaner

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize content cleaner
cleaner = ContentCleaner()

def is_valid_url(url):
    """Validate if the URL is properly formatted and accessible"""
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ['http', 'https'], parsed.netloc])
    except Exception:
        return False

def normalize_url(url):
    """Normalize URL by adding scheme if missing"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

@app.route('/')
def index():
    """Main page with URL input form"""
    return render_template('index.html')

@app.route('/mirror', methods=['POST'])
def mirror_page():
    """Process URL and return cleaned content"""
    url = request.form.get('url', '').strip()
    
    if not url:
        flash('Please enter a URL', 'error')
        return redirect(url_for('index'))
    
    # Normalize and validate URL
    url = normalize_url(url)
    if not is_valid_url(url):
        flash('Please enter a valid URL', 'error')
        return redirect(url_for('index'))
    
    try:
        # Set headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Fetch the webpage with timeout and redirect limits
        session = requests.Session()
        session.max_redirects = 5
        response = session.get(
            url, 
            headers=headers, 
            timeout=30, 
            allow_redirects=True
        )
        response.raise_for_status()
        
        # Get the final URL after redirects
        final_url = response.url
        
        # Clean the content
        cleaned_html, original_title = cleaner.clean_content(response.text, final_url)
        
        if not cleaned_html:
            flash('Unable to extract content from the webpage', 'error')
            return redirect(url_for('index'))
        
        return render_template('result.html', 
                             content=cleaned_html, 
                             original_url=url,
                             final_url=final_url,
                             title=original_title)
    
    except Timeout:
        flash('Request timed out. The website took too long to respond.', 'error')
    except ConnectionError:
        flash('Unable to connect to the website. Please check the URL.', 'error')
    except requests.exceptions.TooManyRedirects:
        flash('Too many redirects. The website may have a redirect loop.', 'error')
    except requests.exceptions.HTTPError as e:
        flash(f'HTTP Error {e.response.status_code}: Unable to access the webpage.', 'error')
    except RequestException as e:
        flash(f'Error fetching the webpage: {str(e)}', 'error')
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        flash('An unexpected error occurred while processing the webpage.', 'error')
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
