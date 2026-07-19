"""
Synchronization Service for TallySync

Handles all data synchronization between Tally and local database.

Author: OmniMagination
Version: 1.0.0
"""

from typing import Dict, Any, Optional
from datetime import datetime

from app.core.logger import logger
from app.core.exceptions import SyncError
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
    """Service for synchronizing data from Tally to local database."""
    
    def __init__(self) -> None:
        """Initialize sync service."""
        self.client = TallyClient()
        self.client.timeout = 60  # Increase timeout
        self.company_repo = CompanyRepository()
        self.ledger_repo = LedgerRepository()
        self.voucher_repo = VoucherRepository()
        self.sync_log_repo = SyncLogRepository()
        
        logger.info("SyncService initialized", category="sync")
    
    def test_connection(self) -> bool:
        """Test connection to Tally server."""
        return self.client.test_connection()
    
    def sync_companies(self) -> Dict[str, Any]:
        """Sync all companies from Tally."""
        sync_type = "companies"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_id = self.sync_log_repo.create_log(sync_type, start_time)
        logger.log_sync_start(sync_type)
        
        result = {"success": False, "records_processed": 0, "records_failed": 0, "error": None}
        
        try:
            xml_request = XMLBuilder.get_company_info_request()
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                raise SyncError("No response from Tally server", sync_type=sync_type)
            
            companies = XMLParser.parse_companies(xml_response)
            
            for company_data in companies:
                try:
                    if not self.company_repo.exists("company_id", company_data["company_id"]):
                        self.company_repo.create(company_data)
                    else:
                        self.company_repo.update_by_field("company_id", company_data["company_id"], company_data)
                    result["records_processed"] += 1
                except Exception as e:
                    logger.error(f"Failed to save company: {e}", category="sync")
                    result["records_failed"] += 1
            
            result["success"] = result["records_failed"] == 0
            logger.log_sync_complete(sync_type, result["records_processed"])
        
        except Exception as e:
            result["error"] = str(e)
            logger.log_sync_error(sync_type, str(e))
            logger.warning(f"Company sync skipped: {e}", category="sync")
        
        self.sync_log_repo.update_log(log_id, "success" if result["success"] else "partial", result["records_processed"], result["records_failed"], result["error"] or "")
        return result
    
    def sync_ledgers(self, company_id: str = "") -> Dict[str, Any]:
        """Sync all ledgers from Tally."""
        sync_type = "ledgers"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_id = self.sync_log_repo.create_log(sync_type, start_time)
        logger.log_sync_start(sync_type)
        
        result = {"success": False, "records_processed": 0, "records_failed": 0, "error": None}
        
        try:
            xml_request = XMLBuilder.get_ledgers_request()
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                raise SyncError("No response from Tally server", sync_type=sync_type)
            
            if "LINEERROR" in xml_response.upper():
                raise SyncError(f"Tally error: {xml_response[:200]}", sync_type=sync_type)
            
            ledgers = XMLParser.parse_ledgers(xml_response, company_id)
            
            for ledger_data in ledgers:
                try:
                    if not self.ledger_repo.exists("ledger_id", ledger_data["ledger_id"]):
                        self.ledger_repo.create(ledger_data)
                    else:
                        self.ledger_repo.update_by_field("ledger_id", ledger_data["ledger_id"], ledger_data)
                    result["records_processed"] += 1
                except Exception as e:
                    logger.error(f"Failed to save ledger: {e}", category="sync")
                    result["records_failed"] += 1
            
            result["success"] = result["records_failed"] == 0
            logger.log_sync_complete(sync_type, result["records_processed"])
        
        except Exception as e:
            result["error"] = str(e)
            logger.log_sync_error(sync_type, str(e))
        
        self.sync_log_repo.update_log(log_id, "success" if result["success"] else "failed", result["records_processed"], result["records_failed"], result["error"] or "")
        return result
    
    def sync_vouchers(self, company_id: str = "") -> Dict[str, Any]:
        """Sync all vouchers from Tally - OPTIONAL FEATURE."""
        sync_type = "vouchers"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_id = self.sync_log_repo.create_log(sync_type, start_time)
        logger.log_sync_start(sync_type)
        
        result = {"success": False, "records_processed": 0, "records_failed": 0, "error": None, "skipped": False}
        
        try:
            xml_request = XMLBuilder.get_vouchers_request()
            xml_response = self.client.send_request(xml_request)
            
            if not xml_response:
                result["skipped"] = True
                result["error"] = "No response - Voucher sync may require TDL file"
                logger.warning("Voucher sync skipped - No response from Tally", category="sync")
                self.sync_log_repo.update_log(log_id, "skipped", 0, 0, result["error"])
                return result
            
            if "LINEERROR" in xml_response.upper() or "Could not find" in xml_response:
                result["skipped"] = True
                result["error"] = "Voucher export requires TDL configuration in Tally"
                logger.warning("Voucher sync skipped - Tally TDL error", category="sync")
                self.sync_log_repo.update_log(log_id, "skipped", 0, 0, result["error"])
                return result
            
            vouchers = XMLParser.parse_vouchers(xml_response, company_id)
            
            for voucher_data in vouchers:
                try:
                    if not self.voucher_repo.exists("voucher_id", voucher_data["voucher_id"]):
                        self.voucher_repo.create(voucher_data)
                    else:
                        self.voucher_repo.update_by_field("voucher_id", voucher_data["voucher_id"], voucher_data)
                    result["records_processed"] += 1
                except Exception as e:
                    result["records_failed"] += 1
            
            result["success"] = True
            logger.log_sync_complete(sync_type, result["records_processed"])
        
        except Exception as e:
            result["error"] = str(e)
            result["skipped"] = True
            logger.warning(f"Voucher sync skipped: {e}", category="sync")
        
        status = "skipped" if result["skipped"] else ("success" if result["success"] else "failed")
        self.sync_log_repo.update_log(log_id, status, result["records_processed"], result["records_failed"], result["error"] or "")
        return result
    
    def full_sync(self) -> Dict[str, Any]:
        """Perform full synchronization."""
        logger.info("Starting full synchronization", category="sync")
        
        results = {
            "companies": self.sync_companies(),
            "ledgers": self.sync_ledgers(),
            "vouchers": self.sync_vouchers(),
        }
        
        total_processed = sum(r["records_processed"] for r in results.values())
        total_failed = sum(r["records_failed"] for r in results.values())
        skipped = sum(1 for r in results.values() if r.get("skipped", False))
        
        results["summary"] = {
            "success": all(r.get("success", False) or r.get("skipped", False) for r in results.values()),
            "total_processed": total_processed,
            "total_failed": total_failed,
            "skipped": skipped,
        }
        
        logger.info(f"Full sync completed: {total_processed} processed, {total_failed} failed, {skipped} skipped", category="sync")
        return results
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status."""
        recent_logs = self.sync_log_repo.get_recent(limit=10)
        stats = self.sync_log_repo.get_stats()
        return {
            "total_syncs": stats["total"],
            "successful_syncs": stats["success"],
            "failed_syncs": stats["failed"],
            "success_rate": stats["success_rate"],
            "recent_logs": [log.to_dict() for log in recent_logs],
        }
