#!/usr/bin/env python
"""
Application startup verification script
验证应用程序启动和配置
"""

import sys
import os
from pathlib import Path

def verify_startup():
    """Verify that the application starts successfully"""
    
    # Add project to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    print("=" * 60)
    print("Academic Paper Analysis System - Startup Verification")
    print("=" * 60)
    
    checks = {
        "Configuration": False,
        "Models": False,
        "Paper Parser Agent": False,
        "Math Model Agent": False,
        "Domain Analyzer Agent": False,
        "Scholar Analyzer Agent": False,
        "Tech Roadmap Agent": False,
        "Main Orchestrator": False,
    }
    
    try:
        print("\n1. Loading configuration...")
        from app.config import settings
        checks["Configuration"] = bool(settings.OPENAI_API_KEY)
        print(f"   - OPENAI_API_KEY loaded: {checks['Configuration']}")
        print(f"   - Model: {settings.OPENAI_MODEL}")
        
        print("\n2. Loading data models...")
        from app.models.schemas import PaperInput
        checks["Models"] = True
        print("   - PaperInput model loaded successfully")
        
        print("\n3. Loading agents...")
        from app.agents.paper_parser import PaperParserAgent
        checks["Paper Parser Agent"] = True
        print("   - PaperParserAgent imported")
        
        from app.agents.math_model_agent import MathModelAgent
        checks["Math Model Agent"] = True
        print("   - MathModelAgent imported")
        
        from app.agents.domain_analyzer import DomainAnalyzerAgent
        checks["Domain Analyzer Agent"] = True
        print("   - DomainAnalyzerAgent imported")
        
        from app.agents.scholar_analyzer import ScholarAnalyzerAgent
        checks["Scholar Analyzer Agent"] = True
        print("   - ScholarAnalyzerAgent imported")
        
        from app.agents.tech_roadmap import TechRoadmapAgent
        checks["Tech Roadmap Agent"] = True
        print("   - TechRoadmapAgent imported")
        
        print("\n4. Initializing main orchestrator...")
        from app.agents.orchestrator import AcademicAnalysisOrchestrator
        orchestrator = AcademicAnalysisOrchestrator()
        checks["Main Orchestrator"] = True
        print("   - AcademicAnalysisOrchestrator initialized successfully")
        print("   - Note: Individual agents use lazy initialization")
        
        print("\n" + "=" * 60)
        print("VERIFICATION RESULTS")
        print("=" * 60)
        
        for check_name, passed in checks.items():
            status = "[OK]" if passed else "[FAILED]"
            print(f"{status} {check_name}")
        
        all_passed = all(checks.values())
        
        print("=" * 60)
        if all_passed:
            print("SUCCESS: Application is ready to run!")
            print("\nTo start the server, run:")
            print("  python -m uvicorn app.main:app --reload")
            return 0
        else:
            print("FAILURE: Some checks did not pass")
            return 1
            
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(verify_startup())
