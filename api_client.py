import requests
import json
import logging
from typing import List, Dict, Optional
from config import API_URL, VIEW_URL_BASE, SEARCH_PAYLOAD

logger = logging.getLogger(__name__)


class AbandonedObjectsAPI:
    """Client for working with abandoned objects API"""
    
    def __init__(self):
        self.api_url = API_URL
        self.view_url_base = VIEW_URL_BASE
        # Use configured search payload
        self.payload = SEARCH_PAYLOAD.copy()
    
    def fetch_abandoned_objects(self) -> Optional[List[Dict]]:
        """
        Fetch abandoned objects from the API
        
        Returns:
            List of abandoned objects or None if error occurred
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
                'Origin': 'https://eri2.nca.by',
                'Referer': 'https://eri2.nca.by/'
            }
            
            # Convert payload to JSON string with proper formatting
            json_payload = json.dumps(self.payload)
            logger.info(f"Sending request with payload: {json_payload}")
            
            response = requests.post(
                self.api_url,
                data=json_payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API response received successfully")
            
            if data.get('data') and data['data'].get('content'):
                content = data['data']['content']
                if content:  # Check if content is not empty/null
                    logger.info(f"Found {len(content)} objects")
                    return content
                else:
                    logger.info("API returned empty content - no objects match the search criteria")
                    return []
            else:
                logger.info("No content found in API response")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def get_view_url(self, object_id: int) -> str:
        """
        Generate view URL for specific abandoned object
        
        Args:
            object_id: ID of the abandoned object
            
        Returns:
            Complete URL for viewing the object
        """
        return f"{self.view_url_base}/{object_id}/forView"
    
    def extract_object_ids(self, objects: List[Dict]) -> List[int]:
        """
        Extract IDs from list of abandoned objects
        
        Args:
            objects: List of abandoned objects
            
        Returns:
            List of object IDs
        """
        return [obj.get('id') for obj in objects if obj.get('id')]
