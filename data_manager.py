import json
import os
import logging
from typing import List, Dict, Set
from config import DATA_FILE

logger = logging.getLogger(__name__)


class DataManager:
    """Manager for handling data persistence and comparison"""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
    
    def load_last_ids(self) -> Set[int]:
        """
        Load last saved object IDs from file
        
        Returns:
            Set of previously saved object IDs
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('last_ids', []))
            else:
                logger.info(f"Data file {self.data_file} does not exist, starting fresh")
                return set()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading data file: {e}")
            return set()
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            return set()
    
    def save_current_ids(self, object_ids: List[int]) -> bool:
        """
        Save current object IDs to file
        
        Args:
            object_ids: List of current object IDs
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            data = {
                'last_ids': list(set(object_ids)),  # Remove duplicates
                'last_update': self._get_current_timestamp()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(object_ids)} IDs to {self.data_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving data file: {e}")
            return False
    
    def get_new_objects(self, current_objects: List[Dict]) -> List[Dict]:
        """
        Compare current objects with last saved and return only new ones
        
        Args:
            current_objects: List of current abandoned objects
            
        Returns:
            List of new objects not seen before
        """
        if not current_objects:
            return []
        
        last_ids = self.load_last_ids()
        current_ids = {obj.get('id') for obj in current_objects if obj.get('id')}
        
        # Find new IDs that weren't in the last check
        new_ids = current_ids - last_ids
        
        # Filter objects to only include new ones
        new_objects = [obj for obj in current_objects if obj.get('id') in new_ids]
        
        logger.info(f"Found {len(new_objects)} new objects out of {len(current_objects)} total")
        
        # Save current state for next comparison
        if current_ids:
            self.save_current_ids(list(current_ids))
        
        return new_objects
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as ISO string"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_last_update_info(self) -> Dict:
        """
        Get information about last update
        
        Returns:
            Dictionary with last update information
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        'last_update': data.get('last_update'),
                        'objects_count': len(data.get('last_ids', []))
                    }
            else:
                return {'last_update': None, 'objects_count': 0}
        except Exception as e:
            logger.error(f"Error getting last update info: {e}")
            return {'last_update': None, 'objects_count': 0}
