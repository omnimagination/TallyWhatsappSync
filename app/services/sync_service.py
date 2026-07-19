"""
Synchronization Service for TallySync

Handles all data synchronization between Tally and local database.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Dict, Any, Optional
from datetime import datetime

from app.core.logger import logger
from app.core.exceptions import SyncError, TallyConnectionError
from app.database.repositories import (
    CompanyRepository,
    LedgerRepository,
    VoucherRepository,
    SyncLogRepository,
)
from app.services.tally_client import TallyClient
from app.services.xml_builder import XMLBuilder
from app.services.xml_parser import XMLParser


class SyncService:
    """
    Service for synchronizing data from Tally to local database.
    
    Features:
    - Initial full sync
    - Scheduled incremental sync
    - On-demand ledger sync
    - Sync logging and tracking
    """
    
    def __init__(self) -> None:
        """Initialize sync service."""
        self.client = TallyClient()
        self.company_repo = CompanyRepository()
        self.ledger_repo = LedgerRepository()
        self.voucher_repo = VoucherRepository()
        self.sync_log_repo = SyncLogRepository()
        
        logger.info("SyncService initialized", category="sync")
    
    def test_connection(self) -> bool:
        """
        Test connection to Tally server.
        
        Returns:
            True if connection successful
        """
        return self.client.test_connection()
    
    def sync_companies(self) -> Dict[str, Any]:
        """
        Sync all companies from Tally.
        
        Returns:
            Sync result statistics
        """
        sync_type = "companies"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_id = self.sync_log_repo.create_log(sync_type, start_time)
        logger.log_sync_start(sync_type)
        
        result = {
            "success": False,
            "records_processed": 0,
            "records_failed": 0,
            "error": None,
        }
        
        try:
            # Get companies from Tally
            xml_request = XMLBuilder.get_all_companies_request()
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                raise SyncError("No response from Tally server", sync_type=sync_type)
            
            if not XMLParser.is_valid_response(xml_response):
                error_msg = XMLParser.get_error_message(xml_response)
                raise SyncError(f"Tally error: {error_msg}", sync_type=sync_type)
            
            # Parse companies
            companies = XMLParser.parse_companies(xml_response)
            
            # Save to database
            for company_data in companies:
                try:
                    if not self.company_repo.exists("company_id", company_data["company_id"]):
                        self.company_repo.create(company_data)
                        result["records_processed"] += 1
                    else:
                        self.company_repo.update_by_field(
                            "company_id",
                            company_data["company_id"],
                            company_data,
                        )
                        result["records_processed"] += 1
                except Exception as e:
                    logger.error(f"Failed to save company: {e}", category="sync")
                    result["records_failed"] += 1
            
            result["success"] = result["records_failed"] == 0
            logger.log_sync_complete(sync_type, result["records_processed"])
        
        except Exception as e:
            result["error"] = str(e)
            logger.log_sync_error(sync_type, str(e))
        
        # Update sync log
        status = "success" if result["success"] else "failed"
        self.sync_log_repo.update_log(
            log_id,
            status,
            result["records_processed"],
            result["records_failed"],
            result["error"] or "",
        )
        
        return result
    
    def sync_ledgers(self, company_id: str = "") -> Dict[str, Any]:
        """
        Sync all ledgers from Tally.
        
        Args:
            company_id: Specific company ID (empty = all)
        
        Returns:
            Sync result statistics
        """
        sync_type = "ledgers"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_id = self.sync_log_repo.create_log(sync_type, start_time)
        logger.log_sync_start(sync_type)
        
        result = {
            "success": False,
            "records_processed": 0,
            "records_failed": 0,
            "error": None,
        }
        
        try:
            # Get ledgers from Tally
            xml_request = XMLBuilder.get_ledgers_request(company_id)
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                raise SyncError("No response from Tally server", sync_type=sync_type)
            
            # Parse ledgers
            ledgers = XMLParser.parse_ledgers(xml_response, company_id)
            
            # Save to database
            for ledger_data in ledgers:
                try:
                    if not self.ledger_repo.exists("ledger_id", ledger_data["ledger_id"]):
                        self.ledger_repo.create(ledger_data)
                        result["records_processed"] += 1
                    else:
                        self.ledger_repo.update_by_field(
                            "ledger_id",
                            ledger_data["ledger_id"],
                            ledger_data,
                        )
                        result["records_processed"] += 1
                except Exception as e:
                    logger.error(f"Failed to save ledger: {e}", category="sync")
                    result["records_failed"] += 1
            
            result["success"] = result["records_failed"] == 0
            logger.log_sync_complete(sync_type, result["records_processed"])
        
        except Exception as e:
            result["error"] = str(e)
            logger.log_sync_error(sync_type, str(e))
        
        # Update sync log
        status = "success" if result["success"] else "failed"
        self.sync_log_repo.update_log(
            log_id,
            status,
            result["records_processed"],
            result["records_failed"],
            result["error"] or "",
        )
        
        return result
    
    def sync_vouchers(self, company_id: str = "") -> Dict[str, Any]:
        """
        Sync all vouchers from Tally.
        
        Args:
            company_id: Specific company ID (empty = all)
        
        Returns:
            Sync result statistics
        """
        sync_type = "vouchers"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_id = self.sync_log_repo.create_log(sync_type, start_time)
        logger.log_sync_start(sync_type)
        
        result = {
            "success": False,
            "records_processed": 0,
            "records_failed": 0,
            "error": None,
        }
        
        try:
            # Get vouchers from Tally
            xml_request = XMLBuilder.get_vouchers_request(company_id)
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                raise SyncError("No response from Tally server", sync_type=sync_type)
            
            # Parse vouchers
            vouchers = XMLParser.parse_vouchers(xml_response, company_id)
            
            # Save to database
            for voucher_data in vouchers:
                try:
                    if not self.voucher_repo.exists("voucher_id", voucher_data["voucher_id"]):
                        self.voucher_repo.create(voucher_data)
                        result["records_processed"] += 1
                    else:
                        self.voucher_repo.update_by_field(
                            "voucher_id",
                            voucher_data["voucher_id"],
                            voucher_data,
                        )
                        result["records_processed"] += 1
                except Exception as e:
                    logger.error(f"Failed to save voucher: {e}", category="sync")
                    result["records_failed"] += 1
            
            result["success"] = result["records_failed"] == 0
            logger.log_sync_complete(sync_type, result["records_processed"])
        
        except Exception as e:
            result["error"] = str(e)
            logger.log_sync_error(sync_type, str(e))
        
        # Update sync log
        status = "success" if result["success"] else "failed"
        self.sync_log_repo.update_log(
            log_id,
            status,
            result["records_processed"],
            result["records_failed"],
            result["error"] or "",
        )
        
        return result
    
    def sync_ledger_on_demand(self, ledger_name: str) -> Dict[str, Any]:
        """
        Sync specific ledger on demand (for search/validation).
        
        Args:
            ledger_name: Ledger name to sync
        
        Returns:
            Sync result
        """
        sync_type = "ledger_on_demand"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result = {
            "success": False,
            "ledger_data": None,
            "error": None,
        }
        
        try:
            # Get ledger from Tally
            xml_request = XMLBuilder.get_ledger_detail_request(ledger_name)
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                raise SyncError("No response from Tally server", sync_type=sync_type)
            
            # Parse ledger
            ledgers = XMLParser.parse_ledgers(xml_response)
            
            if ledgers:
                ledger_data = ledgers[0]
                
                # Update database
                if self.ledger_repo.exists("ledger_id", ledger_data["ledger_id"]):
                    self.ledger_repo.update_by_field(
                        "ledger_id",
                        ledger_data["ledger_id"],
                        ledger_data,
                    )
                else:
                    self.ledger_repo.create(ledger_data)
                
                result["success"] = True
                result["ledger_data"] = ledger_data
                logger.info(f"Ledger synced on-demand: {ledger_name}", category="sync")
        
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Failed to sync ledger on-demand: {e}", category="sync")
        
        return result
    
    def full_sync(self) -> Dict[str, Any]:
        """
        Perform full synchronization (companies + ledgers + vouchers).
        
        Returns:
            Combined sync results
        """
        logger.info("Starting full synchronization", category="sync")
        
        results = {
            "companies": self.sync_companies(),
            "ledgers": self.sync_ledgers(),
            "vouchers": self.sync_vouchers(),
        }
        
        total_processed = sum(r["records_processed"] for r in results.values())
        total_failed = sum(r["records_failed"] for r in results.values())
        
        results["summary"] = {
            "success": all(r["success"] for r in results.values()),
            "total_processed": total_processed,
            "total_failed": total_failed,
        }
        
        logger.info(
            f"Full sync completed: {total_processed} processed, {total_failed} failed",
            category="sync",
        )
        
        return results
    
    def get_sync_status(self) -> Dict[str, Any]:
        """
        Get current sync status.
        
        Returns:
            Sync status information
        """
        recent_logs = self.sync_log_repo.get_recent(limit=10)
        stats = self.sync_log_repo.get_stats()
        
        return {
            "total_syncs": stats["total"],
            "successful_syncs": stats["success"],
            "failed_syncs": stats["failed"],
            "success_rate": stats["success_rate"],
            "recent_logs": [log.to_dict() for log in recent_logs],
        }
