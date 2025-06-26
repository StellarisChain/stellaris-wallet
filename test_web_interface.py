#!/usr/bin/env python3
"""
Simple test to verify web interface functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test the main API endpoints"""
    
    print("Testing Stellaris Wallet Web Interface...")
    
    # Test wallet status
    print("\n1. Testing wallet status...")
    try:
        response = requests.get(f"{BASE_URL}/api/wallet-status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test balance API
    print("\n2. Testing balance API...")
    try:
        # For unencrypted wallet
        response = requests.get(f"{BASE_URL}/api/balance?password=&currency=USD")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            if data.get('success'):
                balance_data = data.get('data', {}).get('balance_data', {})
                print(f"Total Balance: {balance_data.get('total_balance')}")
                print(f"Total USD Value: {balance_data.get('total_usd_value')}")
                print(f"Addresses Count: {len(balance_data.get('addresses', []))}")
            else:
                print(f"Error: {data.get('error')}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test addresses API
    print("\n3. Testing addresses API...")
    try:
        response = requests.get(f"{BASE_URL}/api/addresses?password=")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            if data.get('success'):
                entry_data = data.get('data', {}).get('entry_data', {})
                entries = entry_data.get('entries', [])
                print(f"Addresses found: {len(entries)}")
                if entries:
                    print(f"First address: {entries[0].get('address', 'N/A')}")
            else:
                print(f"Error: {data.get('error')}")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
