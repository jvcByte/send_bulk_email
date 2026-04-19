#!/usr/bin/env python3
"""
Main entry point for bulk email system.

Usage:
    python run.py              # Send to all participants
    python run.py --test       # Send test email
    python run.py --dry-run    # Preview without sending
"""

import sys
import argparse
import config
from src.utils.logger import Logger
from src.utils.config_loader import ConfigLoader
from src.cli.commands import Commands


def main():
    """Main entry point."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Bulk email sender for recording platform credentials'
    )
    parser.add_argument('--test', action='store_true', help='Send test email only')
    parser.add_argument('--dry-run', action='store_true', help='Preview without sending')
    args = parser.parse_args()
    
    # Initialize logger
    logger = Logger(log_file=config.LOG_FILE)
    
    try:
        # Load and validate configuration
        config_loader = ConfigLoader()
        cfg = config_loader.load_from_module(config)
        config_loader.validate_smtp_config(cfg)
        config_loader.validate_platform_config(cfg)
        
        # Initialize commands
        commands = Commands(cfg, logger)
        
        # Execute command
        if args.test:
            success = commands.test()
        elif args.dry_run:
            success = commands.dry_run()
        else:
            success = commands.send()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
