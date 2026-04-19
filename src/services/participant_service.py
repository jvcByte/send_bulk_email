"""
Participant service - handles participant data operations.
Responsibility: Load and manage participant data
"""
import csv
from typing import List, Dict


class ParticipantService:
    """Service for managing participant data."""
    
    @staticmethod
    def load_from_csv(filename: str) -> List[Dict[str, str]]:
        """
        Load participants from CSV file.
        
        Args:
            filename: Path to CSV file
            
        Returns:
            List of participant dictionaries
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV is missing required columns
        """
        participants = []
        required_fields = ['email', 'username', 'password']
        
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                
                # Validate headers
                if not all(field in reader.fieldnames for field in required_fields):
                    raise ValueError(f"CSV must contain columns: {', '.join(required_fields)}")
                
                for row in reader:
                    # Only add rows with all required fields
                    if all(row.get(field) for field in required_fields):
                        participants.append(row)
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Participant file not found: {filename}")
        
        return participants
    
    @staticmethod
    def validate_participant(participant: Dict[str, str]) -> bool:
        """
        Validate participant data.
        
        Args:
            participant: Participant dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['email', 'username', 'password']
        return all(participant.get(field) for field in required_fields)
