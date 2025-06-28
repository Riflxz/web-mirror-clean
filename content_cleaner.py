import re
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin, urlparse
import logging

class ContentCleaner:
    def __init__(self):
        # Ad-related patterns for class names and IDs
        self.ad_patterns = [
            r'.*ad[s]?.*', r'.*advertisement.*', r'.*banner.*', r'.*sponsor.*',
            r'.*promo.*', r'.*popup.*', r'.*modal.*', r'.*overlay.*',
            r'.*sidebar.*', r'.*footer.*', r'.*header.*navigation.*',
            r'.*google.*ad.*', r'.*adsense.*', r'.*adnxs.*', r'.*doubleclick.*',
            r'.*outbrain.*', r'.*taboola.*', r'.*disqus.*', r'.*facebook.*plugin.*',
            r'.*twitter.*widget.*', r'.*social.*share.*', r'.*newsletter.*',
            r'.*subscribe.*', r'.*related.*posts.*', r'.*recommended.*',
            r'.*widget.*', r'.*gadget.*', r'.*plugin.*'
        ]
        
        # Ad network domains to block
        self.ad_domains = [
            'googlesyndication.com', 'googleadservices.com', 'doubleclick.net',
            'googletagmanager.com', 'google-analytics.com', 'scorecardresearch.com',
            'outbrain.com', 'taboola.com', 'adsystem.com', 'amazon-adsystem.com',
            'facebook.com', 'connect.facebook.net', 'twitter.com', 'platform.twitter.com',
            'disqus.com', 'sharethis.com', 'addthis.com', 'quantserve.com',
            'adsafeprotected.com', 'moatads.com', 'turn.com', 'rlcdn.com'
        ]
        
    def is_ad_element(self, element):
        """Check if an element is likely an advertisement"""
        if not element.name:
            return False
            
        # Check class and id attributes
        for attr in ['class', 'id']:
            if element.has_attr(attr):
                attr_value = ' '.join(element[attr]) if isinstance(element[attr], list) else str(element[attr])
                for pattern in self.ad_patterns:
                    if re.match(pattern, attr_value, re.IGNORECASE):
                        return True
        
        # Check data attributes
        for attr in element.attrs:
            if attr.startswith('data-') and any(ad_term in attr.lower() for ad_term in ['ad', 'sponsor', 'promo']):
                return True
                
        return False
    
    def is_ad_script(self, script_tag):
        """Check if a script tag is from an ad network"""
        if not script_tag.has_attr('src'):
            # Check inline scripts for ad-related content
            script_content = script_tag.get_text()
            if any(domain in script_content for domain in self.ad_domains):
                return True
            return False
            
        src = script_tag['src']
        parsed_url = urlparse(src)
        domain = parsed_url.netloc.lower()
        
        return any(ad_domain in domain for ad_domain in self.ad_domains)
    
    def clean_content(self, html_content, base_url):
        """Clean HTML content by removing ads and unwanted elements"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract original title
            title_tag = soup.find('title')
            original_title = title_tag.get_text().strip() if title_tag else "Mirrored Page"
            
            # Remove comments
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()
            
            # Remove script tags from ad networks or with ad-related content
            for script in soup.find_all('script'):
                if self.is_ad_script(script):
                    script.extract()
                    continue
                # Remove scripts with suspicious inline content
                script_text = script.get_text()
                if any(term in script_text.lower() for term in ['adsense', 'doubleclick', 'googletag', 'amazon-adsystem']):
                    script.extract()
            
            # Remove all iframes (often used for ads)
            for iframe in soup.find_all('iframe'):
                iframe.extract()
            
            # Remove elements with ad-related attributes
            for element in soup.find_all():
                if self.is_ad_element(element):
                    element.extract()
            
            # Remove specific problematic tags
            for tag_name in ['noscript', 'object', 'embed', 'applet']:
                for tag in soup.find_all(tag_name):
                    tag.extract()
            
            # Clean up links and images - make them absolute
            self.fix_relative_urls(soup, base_url)
            
            # Remove empty elements
            self.remove_empty_elements(soup)
            
            # Extract main content area
            main_content = self.extract_main_content(soup)
            
            return str(main_content), original_title
            
        except Exception as e:
            logging.error(f"Error cleaning content: {str(e)}")
            return None, None
    
    def fix_relative_urls(self, soup, base_url):
        """Convert relative URLs to absolute URLs"""
        # Fix image sources
        for img in soup.find_all('img', src=True):
            img['src'] = urljoin(base_url, img['src'])
        
        # Fix link hrefs
        for link in soup.find_all('a', href=True):
            link['href'] = urljoin(base_url, link['href'])
        
        # Fix CSS links
        for link in soup.find_all('link', href=True):
            link['href'] = urljoin(base_url, link['href'])
    
    def remove_empty_elements(self, soup):
        """Remove empty elements that serve no purpose"""
        for element in soup.find_all():
            # Skip certain tags that can be legitimately empty
            if element.name in ['br', 'hr', 'img', 'input', 'meta', 'link']:
                continue
                
            # Remove if empty and has no useful attributes
            if not element.get_text(strip=True) and not element.find_all(['img', 'br', 'hr']):
                element.extract()
    
    def extract_main_content(self, soup):
        """Try to extract the main content area of the page"""
        # Try to find main content containers
        main_selectors = [
            'main', 'article', '[role="main"]', '.main', '.content', 
            '.post-content', '.entry-content', '.article-content',
            '.page-content', '.single-content', '.post-body'
        ]
        
        for selector in main_selectors:
            main_element = soup.select_one(selector)
            if main_element and main_element.get_text(strip=True):
                return main_element
        
        # If no main content found, try to find the largest content div
        content_divs = []
        for div in soup.find_all('div'):
            text_length = len(div.get_text(strip=True))
            if text_length > 200:  # Minimum content length
                content_divs.append((div, text_length))
        
        if content_divs:
            # Return the div with most content
            content_divs.sort(key=lambda x: x[1], reverse=True)
            return content_divs[0][0]
        
        # Last resort: return body content
        body = soup.find('body')
        return body if body else soup
