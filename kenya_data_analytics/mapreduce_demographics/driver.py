#!/usr/bin/env python3
"""
MapReduce Driver for Kenya County Demographics Analysis
Simulates Hadoop MapReduce locally for development/testing
"""
import subprocess
import sys
from pathlib import Path
from typing import Optional


def run_mapreduce(
    input_file: Path,
    mapper_script: Path,
    reducer_script: Path,
    output_file: Optional[Path] = None
) -> None:
    """
    Execute MapReduce job locally using Unix pipes.
    
    Simulates Hadoop streaming by chaining:
    1. Cat input file
    2. Pipe to mapper
    3. Sort intermediate output (shuffle phase)
    4. Pipe to reducer
    
    Args:
        input_file: Path to input CSV file
        mapper_script: Path to mapper.py
        reducer_script: Path to reducer.py
        output_file: Optional output file (default: stdout)
    """
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    if not mapper_script.exists():
        print(f"❌ Error: Mapper script not found: {mapper_script}", file=sys.stderr)
        sys.exit(1)
        
    if not reducer_script.exists():
        print(f"❌ Error: Reducer script not found: {reducer_script}", file=sys.stderr)
        sys.exit(1)
    
    print(f"🚀 Starting MapReduce job...")
    print(f"   Input:   {input_file}")
    print(f"   Mapper:  {mapper_script}")
    print(f"   Reducer: {reducer_script}")
    print()
    
    try:
        # On Windows, we'll use Python subprocess instead of shell pipes
        # Step 1: Run mapper
        with open(input_file, 'r') as input_stream:
            mapper_process = subprocess.Popen(
                [sys.executable, str(mapper_script)],
                stdin=input_stream,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            mapper_output, mapper_errors = mapper_process.communicate()
            
            if mapper_process.returncode != 0:
                print(f"❌ Mapper failed: {mapper_errors}", file=sys.stderr)
                sys.exit(1)
        
        # Step 2: Sort (shuffle phase)
        sorted_output = '\n'.join(sorted(mapper_output.strip().split('\n')))
        
        # Step 3: Run reducer
        reducer_process = subprocess.Popen(
            [sys.executable, str(reducer_script)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        reducer_output, reducer_errors = reducer_process.communicate(input=sorted_output)
        
        if reducer_process.returncode != 0:
            print(f"❌ Reducer failed: {reducer_errors}", file=sys.stderr)
            sys.exit(1)
        
        # Output results
        if output_file:
            with open(output_file, 'w') as out:
                out.write(reducer_output)
            print(f"✅ Results written to: {output_file}")
        else:
            print(reducer_output)
            
        print(f"\n✅ MapReduce job completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running MapReduce: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for MapReduce driver."""
    # Determine project paths
    script_dir = Path(__file__).parent
    datasets_dir = script_dir.parent / 'datasets'
    
    input_file = datasets_dir / 'kenya_county_demographics.csv'
    mapper_script = script_dir / 'mapper.py'
    reducer_script = script_dir / 'reducer.py'
    output_file = script_dir / 'output.txt'
    
    # Allow command-line override
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])
    
    run_mapreduce(input_file, mapper_script, reducer_script, output_file)


if __name__ == '__main__':
    main()
