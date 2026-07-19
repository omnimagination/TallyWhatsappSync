"""
Tally HTTP Client for TallySync

Handles HTTP communication with TallyPrime XML server.

Author: OmniMagination
Version: 1.0.0
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime

from app.core.config import config
from app.core.logger import logger
from app.core.exceptions import TallyConnectionError, TimeoutError


class TallyClient:
    """
    HTTP client for communicating with TallyPrime XML server.
    
    Features:
    - Configurable connection settings
    - Automatic retry on failure
    - Request/response logging
    - Timeout handling
    """
    
    def __init__(self) -> None:
        """Initialize Tally client with configuration."""
        self.base_url = config.get_tally_url()
        self.timeout = config.get("tally", "timeout", default=30)
        self.retry_attempts = config.get("tally", "retry_attempts", default=3)
        self.retry_delay = config.get("tally", "retry_delay", default=2)
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/xml",
            "Accept": "application/xml",
        })
        
        logger.info(f"TallyClient initialized: {self.base_url}", category="xml")
    
    def send_request(self, xml_data: str) -> Optional[str]:
        """
        Send XML request to Tally server.
        
        Args:
            xml_data: XML request string
        
        Returns:
            XML response string or None
        
        Raises:
            TallyConnectionError: If connection fails
            TimeoutError: If request times out
        """
        url = f"{self.base_url}"
        
        for attempt in range(1, self.retry_attempts + 1):
            try:
                logger.log_xml_request(url, "POST")
                
                start_time = datetime.now()
                response = self.session.post(
                    url,
                    data=xml_data,
                    timeout=self.timeout,
                )
                elapsed = (datetime.now() - start_time).total_seconds()
                
                logger.log_xml_response(url, response.status_code, len(response.text))
                logger.debug(f"Request completed in {elapsed:.2f}s", category="xml")
                
                if response.status_code == 200:
                    return response.text
                else:
                    logger.warning(
                        f"Tally returned status {response.status_code}",
                        category="xml",
                    )
                    return None
            
            except requests.exceptions.Timeout:
                logger.warning(
                    f"Request timeout (attempt {attempt}/{self.retry_attempts})",
                    category="xml",
                )
                if attempt == self.retry_attempts:
                    raise TimeoutError(
                        f"Tally request timed out after {self.timeout}s",
                        operation="XML Request",
                        timeout_seconds=self.timeout,
                    )
            
            except requests.exceptions.ConnectionError as e:
                logger.warning(
                    f"Connection error (attempt {attempt}/{self.retry_attempts}): {e}",
                    category="xml",
                )
                if attempt == self.retry_attempts:
                    raise TallyConnectionError(
                        f"Failed to connect to Tally at {self.base_url}",
                        url=url,
                    )
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}", category="xml", exc_info=True)
                if attempt == self.retry_attempts:
                    raise TallyConnectionError(
                        f"Tally request failed: {e}",
                        url=url,
                    )
        
        return None
    
    def test_connection(self) -> bool:
        """
        Test connection to Tally server.
        
        Returns:
            True if connection successful
        """
        from app.services.xml_builder import XMLBuilder
        
        try:
            # Send a simple company info request
            xml_request = XMLBuilder.get_company_info_request()
            response = self.send_request(xml_request)
            
            if response and "ENVELOPE" in response.upper():
                logger.info("Tally connection test successful", category="xml")
                return True
            else:
                logger.warning("Tally connection test returned empty/invalid response", category="xml")
                return False
        
        except Exception as e:
            logger.error(f"Tally connection test failed: {e}", category="xml", exc_info=True)
            return False
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get Tally server information.
        
        Returns:
            Dictionary with server info
        """
        return {
            "url": self.base_url,
            "timeout": self.timeout,
            "retry_attempts": self.retry_attempts,
            "connected": self.test_connection(),
        }
    
    def close(self) -> None:
        """Close HTTP session."""
        self.session.close()
        logger.debug("TallyClient session closed", category="xml")
    
    def __enter__(self) -> "TallyClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()


# Global client instance
tally_client = TallyClient()
