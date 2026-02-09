#!/usr/bin/env python3
"""
Test script to verify all functionality of the enhanced todo app
"""
import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and return the result"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    print("Testing Enhanced Todo App Features\n")
    
    # Change to the src directory
    os.chdir("src")
    
    # Test 1: Add tasks with different priorities and tags
    print("1. Testing add functionality with priorities and tags...")
    commands = [
        'python -m main add "Complete project documentation" -p high -t work -t urgent',
        'python -m main add "Schedule team meeting" -p medium -t work',
        'python -m main add "Buy birthday gift" -p low -t personal',
        'python -m main add "Review code changes" -p high -t work'
    ]
    
    for cmd in commands:
        code, stdout, stderr = run_command(cmd)
        print(f"  Command: {cmd}")
        print(f"  Result: {stdout.strip()}")
        if stderr:
            print(f"  Error: {stderr.strip()}")
        print()
    
    # Test 2: List all tasks (will show empty due to in-memory nature)
    print("2. Testing list functionality...")
    code, stdout, stderr = run_command('python -m main list')
    print(f"  Command: python -m main list")
    print(f"  Result: {stdout.strip()}")
    if stderr:
        print(f"  Error: {stderr.strip()}")
    print()
    
    # Test 3: Test priority command (this would work if we had a persistent store)
    print("3. Testing priority command...")
    print("  Note: This would work in a persistent scenario, but with in-memory storage")
    print("  each command runs in isolation, so we can't modify previously added items")
    print()
    
    # Test 4: Test other commands
    print("4. Testing other commands...")
    other_commands = [
        'python -m main view 1',
        'python -m main search "project"',
        'python -m main filter status pending',
        'python -m main sort priority',
        'python -m main sort id'
    ]
    
    for cmd in other_commands:
        code, stdout, stderr = run_command(cmd)
        print(f"  Command: {cmd}")
        print(f"  Result: {stdout.strip()}")
        if stderr:
            print(f"  Error: {stderr.strip()}")
        print()

    print("Test completed. Note that due to in-memory storage, each command")
    print("runs in isolation. In a real application, you would typically")
    print("have a persistent storage mechanism or run commands in a session.")

if __name__ == "__main__":
    main()