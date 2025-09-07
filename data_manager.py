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
                    # Поддерживаем оба формата: новый (last_checked_ids) и старый (last_ids)
                    ids = data.get('last_checked_ids', data.get('last_ids', []))
                    return set(ids)
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
                'last_checked_ids': list(set(object_ids)),  # Remove duplicates
                'last_update': self._get_current_timestamp(),
                'objects_count': len(set(object_ids))
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
        """Get current timestamp as ISO string in Minsk timezone (UTC+3)"""
        from datetime import datetime, timezone, timedelta
        # Минское время UTC+3
        minsk_tz = timezone(timedelta(hours=3))
        return datetime.now(minsk_tz).isoformat()
    
    def update_last_check_time(self) -> bool:
        """
        Update only the last check time without changing IDs
        Used when check is performed but no new objects found
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Load existing data
            data = {'last_checked_ids': [], 'objects_count': 0}
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Update only the timestamp
            data['last_update'] = self._get_current_timestamp()
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("Updated last check time")
            return True
            
        except Exception as e:
            logger.error(f"Error updating last check time: {e}")
            return False
    
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
                    # Поддерживаем оба формата
                    ids = data.get('last_checked_ids', data.get('last_ids', []))
                    return {
                        'last_update': data.get('last_update'),
                        'objects_count': data.get('objects_count', len(ids))
                    }
            else:
                return {'last_update': None, 'objects_count': 0}
        except Exception as e:
            logger.error(f"Error getting last update info: {e}")
            return {'last_update': None, 'objects_count': 0}
