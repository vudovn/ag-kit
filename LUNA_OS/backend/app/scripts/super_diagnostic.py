#!/usr/bin/env python3
"""
LUNA OS — Super Diagnostic Script
Verificação completa de todos os componentes
"""

import os
import sys
import json
import asyncio
import httpx
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.integrations.supabase_client import get_supabase
from app.config import settings
from loguru import logger

# Configuração de cores
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    NC = '\033[0m'  # No Color


class DiagnosticEngine:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'version': '2.2.0',
            'checks': [],
            'score': 0,
            'max_score': 0
        }
        self.db = get_supabase()
        
    def add_check(self, name: str, passed: bool, details: str = "", score: int = 10):
        """Add check result"""
        self.results['checks'].append({
            'name': name,
            'passed': passed,
            'details': details,
            'score': score
        })
        self.results['max_score'] += score
        if passed:
            self.results['score'] += score
            
    def print_header(self, title: str):
        """Print section header"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
        print(f"{Colors.CYAN}{title:^60}{Colors.NC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.NC}\n")
        
    def print_check(self, name: str, passed: bool, details: str = ""):
        """Print check result"""
        icon = f"{Colors.GREEN}✅{Colors.NC}" if passed else f"{Colors.RED}❌{Colors.NC}"
        status = f"{Colors.GREEN}PASS{Colors.NC}" if passed else f"{Colors.RED}FAIL{Colors.NC}"
        print(f"{icon} {name:<50} {status}")
        if details:
            print(f"   {Colors.WHITE}{details}{Colors.NC}")
    
    async def check_backend_health(self) -> Tuple[bool, str]:
        """Check backend health endpoints"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Basic health
                resp = await client.get("http://localhost:8000/health")
                if resp.status_code != 200:
                    return False, f"Health endpoint returned {resp.status_code}"
                
                data = resp.json()
                if data.get('status') != 'healthy':
                    return False, f"Status: {data.get('status')}"
                
                # Detailed health
                resp = await client.get("http://localhost:8000/api/health/status")
                if resp.status_code != 200:
                    return False, f"Detailed health returned {resp.status_code}"
                
                health_data = resp.json()
                details = []
                
                # Supabase
                supabase_status = health_data.get('supabase', {})
                if supabase_status.get('status') == 'connected':
                    latency = supabase_status.get('latency', 0)
                    details.append(f"Supabase: {latency:.0f}ms")
                else:
                    return False, f"Supabase: {supabase_status.get('status')}"
                
                # Evolution
                evolution_status = health_data.get('evolution', {})
                if evolution_status.get('status') in ['connected', 'warning']:
                    details.append(f"Evolution: {evolution_status.get('details', 'OK')}")
                else:
                    return False, f"Evolution: {evolution_status.get('status')}"
                
                return True, " | ".join(details)
                
        except Exception as e:
            return False, str(e)
    
    async def check_frontend_health(self) -> Tuple[bool, str]:
        """Check frontend accessibility"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get("http://localhost:3000")
                if resp.status_code != 200:
                    return False, f"Frontend returned {resp.status_code}"
                
                # Check if HTML contains expected content
                if "Luna" not in resp.text and "Dashboard" not in resp.text:
                    return False, "Frontend doesn't contain expected content"
                
                return True, "Frontend responding normally"
                
        except Exception as e:
            return False, str(e)
    
    async def check_evolution_api(self) -> Tuple[bool, str]:
        """Check Evolution API status"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get("http://localhost:8081")
                # Evolution may return 404 on root, that's OK
                return True, f"Evolution API online (status: {resp.status_code})"
                
        except Exception as e:
            return False, str(e)
    
    def check_supabase_tables(self) -> Tuple[bool, str]:
        """Check if required Supabase tables exist"""
        try:
            required_tables = [
                'clients',
                'whatsapp_messages_history',
                'business_intelligence',
                'learning_log'
            ]
            
            existing_tables = []
            missing_tables = []
            
            for table in required_tables:
                try:
                    result = self.db.table(table).select("count", count="exact").limit(1).execute()
                    existing_tables.append(table)
                except Exception:
                    missing_tables.append(table)
            
            if missing_tables:
                return False, f"Missing tables: {', '.join(missing_tables)}"
            
            return True, f"All tables exist ({len(existing_tables)} tables)"
            
        except Exception as e:
            return False, str(e)
    
    def check_knowledge_base(self) -> Tuple[bool, str]:
        """Check if knowledge base exists and is valid"""
        try:
            kb_path = Path(__file__).parent / "app" / "knowledge" / "data" / "haven.json"
            
            if not kb_path.exists():
                return False, "haven.json not found"
            
            with open(kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            required_keys = ['services', 'professionals', 'faq']
            missing_keys = [k for k in required_keys if k not in data]
            
            if missing_keys:
                return False, f"Missing keys: {', '.join(missing_keys)}"
            
            services_count = len(data.get('services', []))
            professionals_count = len(data.get('professionals', []))
            faq_count = len(data.get('faq', []))
            
            return True, f"Services: {services_count} | Professionals: {professionals_count} | FAQ: {faq_count}"
            
        except Exception as e:
            return False, str(e)
    
    def check_backend_structure(self) -> Tuple[bool, str]:
        """Check backend file structure"""
        try:
            backend_path = Path(__file__).parent
            
            required_dirs = [
                'app/api',
                'app/core',
                'app/integrations',
                'app/knowledge',
                'app/analytics',
                'app/campaigns',
                'app/dojo'
            ]
            
            missing_dirs = []
            for dir_path in required_dirs:
                if not (backend_path / dir_path).exists():
                    missing_dirs.append(dir_path)
            
            if missing_dirs:
                return False, f"Missing directories: {', '.join(missing_dirs)}"
            
            # Count Python files
            py_files = list(backend_path.rglob("*.py"))
            
            return True, f"Structure OK | {len(py_files)} Python files"
            
        except Exception as e:
            return False, str(e)
    
    def check_frontend_structure(self) -> Tuple[bool, str]:
        """Check frontend file structure"""
        try:
            frontend_path = Path(__file__).parent.parent / "frontend"
            
            if not frontend_path.exists():
                return False, "Frontend directory not found"
            
            required_dirs = ['app', 'components', 'lib', 'public']
            missing_dirs = []
            
            for dir_path in required_dirs:
                if not (frontend_path / dir_path).exists():
                    missing_dirs.append(dir_path)
            
            if missing_dirs:
                return False, f"Missing directories: {', '.join(missing_dirs)}"
            
            # Count TSX files
            tsx_files = list((frontend_path / "app").rglob("*.tsx"))
            
            return True, f"Structure OK | {len(tsx_files)} TSX files"
            
        except Exception as e:
            return False, str(e)
    
    def check_environment(self) -> Tuple[bool, str]:
        """Check environment configuration"""
        try:
            env_path = Path(__file__).parent / ".env"
            
            if not env_path.exists():
                return False, ".env file not found"
            
            with open(env_path, 'r') as f:
                env_content = f.read()
            
            required_vars = [
                'SUPABASE_URL',
                'SUPABASE_KEY',
                'EVOLUTION_API_URL',
                'EVOLUTION_API_KEY',
                'OPENROUTER_API_KEY'
            ]
            
            missing_vars = [var for var in required_vars if var not in env_content]
            
            if missing_vars:
                return False, f"Missing env vars: {', '.join(missing_vars)}"
            
            # Check if keys are not default
            if "your-project.supabase.co" in env_content:
                return False, "Using default Supabase URL"
            
            if "your-anthropic-key" in env_content:
                return False, "Using default API keys"
            
            return True, "Environment configured correctly"
            
        except Exception as e:
            return False, str(e)
    
    async def check_api_endpoints(self) -> Tuple[bool, str]:
        """Check critical API endpoints"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                endpoints = [
                    ("/", "Root"),
                    ("/api/health/status", "Health Status"),
                    ("/api/analytics/overview", "Analytics"),
                    ("/api/evolution/maturity", "Evolution Maturity"),
                    ("/api/dojo/scenarios", "Dojo Scenarios"),
                    ("/api/knowledge", "Knowledge Base"),
                ]
                
                working = 0
                failed = []
                
                for endpoint, name in endpoints:
                    try:
                        resp = await client.get(f"http://localhost:8000{endpoint}")
                        if resp.status_code == 200:
                            working += 1
                        else:
                            failed.append(f"{name} ({resp.status_code})")
                    except Exception as e:
                        failed.append(f"{name} ({str(e)})")
                
                if failed:
                    return False, f"{working}/{len(endpoints)} OK | Failed: {', '.join(failed)}"
                
                return True, f"All {len(endpoints)} endpoints responding"
                
        except Exception as e:
            return False, str(e)
    
    def check_logs(self) -> Tuple[bool, str]:
        """Check if logs are being generated"""
        try:
            log_path = Path(__file__).parent / "logs" / "luna_core.log"
            
            if not log_path.exists():
                return False, "Log file not found"
            
            # Check log size
            log_size = log_path.stat().st_size
            log_size_mb = log_size / (1024 * 1024)
            
            # Check if log has recent entries
            with open(log_path, 'r') as f:
                lines = f.readlines()
                if len(lines) < 10:
                    return False, "Log file almost empty"
            
            return True, f"Log OK ({log_size_mb:.2f} MB | {len(lines)} lines)"
            
        except Exception as e:
            return False, str(e)
    
    async def run_full_diagnostic(self):
        """Run complete diagnostic"""
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════════════╗{Colors.NC}")
        print(f"{Colors.CYAN}║  🌙 LUNA OS — SUPER DIAGNOSTIC ENGINE             ║{Colors.NC}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════╝{Colors.NC}")
        print(f"\n{Colors.WHITE}Timestamp: {self.results['timestamp']}{Colors.NC}")
        print(f"{Colors.WHITE}Version: LUNA OS v{self.results['version']}{Colors.NC}\n")
        
        # 1. Backend Health
        self.print_header("BACKEND HEALTH")
        passed, details = await self.check_backend_health()
        self.print_check("Backend Health Endpoints", passed, details)
        self.add_check("Backend Health", passed, details, score=15)
        
        # 2. Frontend Health
        self.print_header("FRONTEND HEALTH")
        passed, details = await self.check_frontend_health()
        self.print_check("Frontend Accessibility", passed, details)
        self.add_check("Frontend Health", passed, details, score=10)
        
        # 3. Evolution API
        self.print_header("EVOLUTION API")
        passed, details = await self.check_evolution_api()
        self.print_check("Evolution API Online", passed, details)
        self.add_check("Evolution API", passed, details, score=10)
        
        # 4. Supabase Tables
        self.print_header("SUPABASE DATABASE")
        passed, details = self.check_supabase_tables()
        self.print_check("Required Tables Exist", passed, details)
        self.add_check("Supabase Tables", passed, details, score=15)
        
        # 5. Knowledge Base
        self.print_header("KNOWLEDGE BASE")
        passed, details = self.check_knowledge_base()
        self.print_check("Knowledge Base Valid", passed, details)
        self.add_check("Knowledge Base", passed, details, score=10)
        
        # 6. Backend Structure
        self.print_header("BACKEND STRUCTURE")
        passed, details = self.check_backend_structure()
        self.print_check("Backend File Structure", passed, details)
        self.add_check("Backend Structure", passed, details, score=5)
        
        # 7. Frontend Structure
        self.print_header("FRONTEND STRUCTURE")
        passed, details = self.check_frontend_structure()
        self.print_check("Frontend File Structure", passed, details)
        self.add_check("Frontend Structure", passed, details, score=5)
        
        # 8. Environment
        self.print_header("ENVIRONMENT")
        passed, details = self.check_environment()
        self.print_check("Environment Configuration", passed, details)
        self.add_check("Environment", passed, details, score=10)
        
        # 9. API Endpoints
        self.print_header("API ENDPOINTS")
        passed, details = await self.check_api_endpoints()
        self.print_check("Critical API Endpoints", passed, details)
        self.add_check("API Endpoints", passed, details, score=10)
        
        # 10. Logs
        self.print_header("LOGS & MONITORING")
        passed, details = self.check_logs()
        self.print_check("Log Generation", passed, details)
        self.add_check("Logs", passed, details, score=10)
        
        # Summary
        self.print_header("DIAGNOSTIC SUMMARY")
        score_pct = (self.results['score'] / self.results['max_score'] * 100) if self.results['max_score'] > 0 else 0
        
        print(f"\n{Colors.WHITE}Total Score: {Colors.GREEN if score_pct >= 80 else Colors.YELLOW if score_pct >= 60 else Colors.RED}")
        print(f"  {self.results['score']}/{self.results['max_score']} ({score_pct:.1f}%){Colors.NC}\n")
        
        passed_checks = sum(1 for c in self.results['checks'] if c['passed'])
        failed_checks = len(self.results['checks']) - passed_checks
        
        print(f"{Colors.GREEN}✅ Passed: {passed_checks}{Colors.NC}")
        print(f"{Colors.RED}❌ Failed: {failed_checks}{Colors.NC}\n")
        
        if score_pct >= 90:
            print(f"{Colors.GREEN}╔════════════════════════════════════════════════════╗{Colors.NC}")
            print(f"{Colors.GREEN}║  🏆 EXCELLENT! LUNA OS is in PEAK PERFORMANCE     ║{Colors.NC}")
            print(f"{Colors.GREEN}╚════════════════════════════════════════════════════╝{Colors.NC}")
        elif score_pct >= 70:
            print(f"{Colors.YELLOW}╔════════════════════════════════════════════════════╗{Colors.NC}")
            print(f"{Colors.YELLOW}║  ⚠️  GOOD! Some improvements needed               ║{Colors.NC}")
            print(f"{Colors.YELLOW}╚════════════════════════════════════════════════════╝{Colors.NC}")
        else:
            print(f"{Colors.RED}╔════════════════════════════════════════════════════╗{Colors.NC}")
            print(f"{Colors.RED}║  ❌ CRITICAL! Immediate attention required         ║{Colors.NC}")
            print(f"{Colors.RED}╚════════════════════════════════════════════════════╝{Colors.NC}")
        
        print()
        
        # Save results
        results_path = Path(__file__).parent / "logs" / "diagnostic_results.json"
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"{Colors.WHITE}Results saved to: {results_path}{Colors.NC}\n")
        
        return self.results


async def main():
    """Main entry point"""
    diagnostic = DiagnosticEngine()
    await diagnostic.run_full_diagnostic()


if __name__ == "__main__":
    asyncio.run(main())
