#!/usr/bin/env python3
"""Main runner script for the Sales API Pipeline"""
import sys
from datetime import datetime
from etl.pipeline import SalesDataPipeline

def main():
    print("=" * 80)
    print("SALES API PIPELINE")
    print("=" * 80)
    print(f"Started: {datetime.now()}")
    print("=" * 80)
    print()
    
    try:
        pipeline = SalesDataPipeline()
        result = pipeline.run_full_pipeline()
        
        print("\n" + "=" * 80)
        print("PIPELINE RESULTS")
        print("=" * 80)
        print(f"Status: {result['status']}")
        
        if result['status'] == 'SUCCESS':
            print(f"Duration: {result['duration']:.2f} seconds")
            return 0
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
