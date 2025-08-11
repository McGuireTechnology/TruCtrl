#!/usr/bin/env python3
"""
Script to test asset classes API with authentication.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def get_auth_token():
    """Get authentication token."""
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_asset_classes_api():
    """Test the asset classes API endpoints."""
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("Could not get auth token")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test GET /controls/asset-classes
    print("Testing GET /controls/asset-classes...")
    try:
        response = requests.get(f"{BASE_URL}/controls/asset-classes", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            asset_classes = response.json()
            print(f"Found {len(asset_classes)} asset classes:")
            for asset_class in asset_classes:
                print(f"  - {asset_class['name']} ({asset_class['short_name']})")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing GET: {e}")
    
    print()
    
    # Test POST /controls/asset-classes
    print("Testing POST /controls/asset-classes...")
    new_asset_class = {
        "name": "Test Asset Class",
        "short_name": "TEST",
        "description": "A test asset class for API testing",
        "color": "#ff5722"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/controls/asset-classes", 
                               headers=headers, 
                               json=new_asset_class)
        print(f"Status: {response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            created = response.json()
            print(f"Created asset class: {created['name']} with ID: {created['id']}")
            
            # Test DELETE the created asset class
            print(f"\nTesting DELETE /controls/asset-classes/{created['id']}...")
            delete_response = requests.delete(f"{BASE_URL}/controls/asset-classes/{created['id']}", 
                                            headers=headers)
            print(f"Delete status: {delete_response.status_code}")
            if delete_response.status_code == 200:
                print("Successfully deleted test asset class")
            else:
                print(f"Delete error: {delete_response.text}")
        else:
            print(f"Create error: {response.text}")
    except Exception as e:
        print(f"Error testing POST: {e}")

if __name__ == "__main__":
    test_asset_classes_api()
