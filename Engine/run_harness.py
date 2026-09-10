"""
================================================================================
ENGINE 2: CENTRALIZED EXECUTION HARNESS
================================================================================
A single unified entry point for:
1. Historical Pipeline (data ingestion and validation)
2. Single-asset optimization & meta-labeling
3. Live Terminal (real-time stream processing)

Usage:
  python -m Engine.run_harness pipeline --symbol BTCUSDT
  python -m Engine.run_harness optimize --asset SOL
  python -m Engine.run_harness live --sync
================================================================================
"""
import argparse
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main():
    parser = argparse.ArgumentParser(description="Trading Engine 2 Centralized Harness")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Pipeline Subparser
    pipeline_parser = subparsers.add_parser("pipeline", help="Run historical data pipeline")
    pipeline_parser.add_argument("--symbol", default="BTCUSDT")
    pipeline_parser.add_argument("--all-symbols", action="store_true")
    
    # Optimize Subparser
    optimize_parser = subparsers.add_parser("optimize", help="Run individual asset optimization")
    optimize_parser.add_argument("--asset", required=False)
    optimize_parser.add_argument("--all-assets", action="store_true")
    
    # Live Subparser
    live_parser = subparsers.add_parser("live", help="Run live terminal monitoring")
    live_parser.add_argument("--sync", action="store_true")
    
    args, unknown = parser.parse_known_args()
    
    if args.command == "pipeline":
        from Engine.run_historical_pipeline import main as pipeline_main
        # Reconstruct args for the inner parser
        new_args = []
        if args.all_symbols:
            new_args.append("--all-symbols")
        else:
            new_args.extend(["--symbol", args.symbol])
        new_args.extend(unknown)
        sys.exit(pipeline_main(new_args))
        
    elif args.command == "optimize":
        from Engine.optimize_individual_assets import run_optimization, ASSETS
        if args.all_assets:
            for ticker in ASSETS:
                run_optimization(ticker)
        elif args.asset:
            run_optimization(args.asset)
        else:
            print("Please specify --asset or --all-assets")
            sys.exit(1)
        
    elif args.command == "live":
        from Engine.run_live_terminal import main as live_main
        # Reconstruct args for the inner parser
        sys.argv = [sys.argv[0]] + unknown
        if args.sync:
            sys.argv.append("--sync")
        sys.exit(live_main())

if __name__ == "__main__":
    main()
