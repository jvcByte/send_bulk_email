"""
Configuration loader - loads and validates configuration.
Responsibility: Load configuration from config file
"""
from typing import Dict, Any


class ConfigLoader:
    """Loads and validates configuration."""
    
    @staticmethod
    def load_from_module(config_module) -> Dict[str, Any]:
        """
        Load configuration from a Python module.
        
        Args:
            config_module: Imported config module
            
        Returns:
            Dictionary of configuration values
        """
        config = {}
        
        # Extract all uppercase attributes (convention for config)
        for attr in dir(config_module):
            if attr.isupper():
                config[attr] = getattr(config_module, attr)
        
        return config
    
    @staticmethod
    def validate_smtp_config(config: Dict[str, Any]) -> bool:
        """
        Validate SMTP configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        required = ['SMTP_SERVER', 'SMTP_PORT', 'SENDER_EMAIL', 'SENDER_PASSWORD']
        
        for key in required:
            if key not in config or not config[key]:
                raise ValueError(f"Missing required configuration: {key}")
        
        return True
    
    @staticmethod
    def validate_platform_config(config: Dict[str, Any]) -> bool:
        """
        Validate platform configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        required = ['PLATFORM_NAME', 'PLATFORM_URL']
        
        for key in required:
            if key not in config or not config[key]:
                raise ValueError(f"Missing required configuration: {key}")
        
        return True
