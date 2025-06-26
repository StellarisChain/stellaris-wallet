#!/usr/bin/env python3
"""
Stellaris Wallet Web GUI - A modern web interface for the Stellaris cryptocurrency wallet.
"""

import os
import sys
import json
import logging
import threading
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, Any

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Import wallet functionality
try:
    from wallet_client import (
        generateAddressHelper, decryptWalletEntries, checkBalance,
        prepareTransaction, get_price_info, validate_and_select_node,
        initialize_wallet, generatePaperWallet
    )
except ImportError:
    print("Error: Could not import wallet_client functions. Please ensure wallet_client.py is in the same directory.")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Global variables
current_wallet = None
wallet_data = {}


@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', 
                         current_wallet=current_wallet,
                         wallet_data=wallet_data)


@app.route('/api/price')
def get_current_price():
    """Get current STE price"""
    try:
        price = get_price_info("USD")
        return jsonify({'success': True, 'price': float(price) if price else 0})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/create-wallet')
def create_wallet_page():
    """Create wallet page"""
    return render_template('create_wallet.html')


@app.route('/api/create-wallet', methods=['POST'])
def create_wallet():
    """Create a new wallet"""
    try:
        data = request.json
        
        # Validate input
        if not data.get('wallet_name'):
            return jsonify({'success': False, 'error': 'Wallet name is required'})
        
        if data.get('encrypt') and not data.get('password'):
            return jsonify({'success': False, 'error': 'Password is required for encrypted wallets'})
        
        if data.get('password') != data.get('confirm_password'):
            return jsonify({'success': False, 'error': 'Passwords do not match'})
        
        # Create wallet
        result = generateAddressHelper(
            filename=f"wallets/{data['wallet_name']}.json",
            password=data.get('password') if data.get('encrypt') else None,
            new_wallet=True,
            encrypt=data.get('encrypt', False),
            use2FA=data.get('use2FA', False),
            deterministic=data.get('deterministic', False),
            mnemonic=data.get('mnemonic') if data.get('mnemonic') else None
        )
        
        if result:
            global current_wallet
            current_wallet = f"wallets/{data['wallet_name']}.json"
            return jsonify({'success': True, 'message': 'Wallet created successfully!'})
        else:
            return jsonify({'success': False, 'error': 'Failed to create wallet'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/load-wallet')
def load_wallet_page():
    """Load wallet page"""
    return render_template('load_wallet.html')


@app.route('/api/load-wallet', methods=['POST'])
def load_wallet():
    """Load an existing wallet"""
    try:
        data = request.json
        wallet_path = data.get('wallet_path')
        
        if not wallet_path:
            return jsonify({'success': False, 'error': 'Wallet path is required'})
        
        # Check if wallet exists
        wallet_exists, filename, encrypted = initialize_wallet(wallet_path)
        
        if not wallet_exists:
            return jsonify({'success': False, 'error': 'Wallet file not found'})
        
        global current_wallet, wallet_data
        current_wallet = wallet_path
        
        # Store wallet metadata
        wallet_data = {
            'path': filename,
            'encrypted': encrypted
        }
        
        return jsonify({
            'success': True, 
            'message': 'Wallet loaded successfully!',
            'encrypted': encrypted
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/balance')
def balance_page():
    """Balance overview page"""
    return render_template('balance.html', current_wallet=current_wallet)


@app.route('/api/balance')
def get_balance():
    """Get wallet balance"""
    try:
        print(f"[DEBUG] get_balance called - current_wallet: {current_wallet}")
        print(f"[DEBUG] wallet_data: {wallet_data}")
        
        if not current_wallet:
            return jsonify({'success': False, 'error': 'No wallet loaded'})
        
        password = request.args.get('password')
        currency = request.args.get('currency', 'USD')
        
        print(f"[DEBUG] password: {password}, currency: {currency}")
        
        # Check if wallet is encrypted
        is_encrypted = wallet_data.get('encrypted', False) if wallet_data else False
        print(f"[DEBUG] is_encrypted: {is_encrypted}")
        
        # For encrypted wallets, password is required
        if is_encrypted and not password:
            return jsonify({'success': False, 'error': 'Password required for encrypted wallet'})
        
        # For non-encrypted wallets, set password to None
        if not is_encrypted:
            password = None
        
        print(f"[DEBUG] final password: {password}")
        
        # Get currency symbol
        currency_symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'BTC': '₿', 'ETH': 'Ξ'
        }
        currency_symbol = currency_symbols.get(currency, '$')
        
        print(f"[DEBUG] Calling checkBalance with filename={current_wallet}")
        
        balance_result = checkBalance(
            filename=current_wallet,
            password=password,
            totp_code=None,
            address=None,
            node=None,
            to_json=True,
            to_file=False,
            currency_code=currency,
            currency_symbol=currency_symbol
        )
        
        #print(f"[DEBUG] checkBalance returned: {type(balance_result)} - {balance_result if balance_result else 'None'}...")
        
        if balance_result:
            return jsonify({'success': True, 'data': balance_result})
        else:
            return jsonify({'success': False, 'error': 'Failed to get balance'})
            
    except Exception as e:
        import traceback
        print(f"[DEBUG] Exception in get_balance: {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


@app.route('/send')
def send_page():
    """Send transaction page"""
    return render_template('send.html', current_wallet=current_wallet)


@app.route('/api/send', methods=['POST'])
def send_transaction():
    """Send a transaction"""
    try:
        if not current_wallet:
            return jsonify({'success': False, 'error': 'No wallet loaded'})
        
        data = request.json
        
        # Check if wallet is encrypted
        is_encrypted = wallet_data.get('encrypted', False) if wallet_data else False
        
        # Validate input
        required_fields = ['from_address', 'to_address', 'amount']
        if is_encrypted:
            required_fields.append('password')
            
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'})
        
        # Get password - None for unencrypted wallets
        password = data.get('password') if is_encrypted else None
        
        # Send transaction
        result = prepareTransaction(
            filename=current_wallet,
            password=password,
            totp_code=data.get('totp_code'),
            amount=data['amount'],
            sender=data['from_address'],
            private_key=None,
            receiver=data['to_address'],
            message=data.get('message', ''),
            node=None
        )
        
        if result:
            return jsonify({
                'success': True, 
                'message': 'Transaction sent successfully!',
                'tx_hash': result.hex() if hasattr(result, 'hex') else str(result)
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to send transaction'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/receive')
def receive_page():
    """Receive page"""
    return render_template('receive.html', current_wallet=current_wallet)


@app.route('/api/addresses')
def get_addresses():
    """Get wallet addresses"""
    try:
        if not current_wallet:
            return jsonify({'success': False, 'error': 'No wallet loaded'})
        
        password = request.args.get('password')
        
        # Check if wallet is encrypted
        is_encrypted = wallet_data.get('encrypted', False) if wallet_data else False
        
        # For encrypted wallets, password is required
        if is_encrypted and not password:
            return jsonify({'success': False, 'error': 'Password required for encrypted wallet'})
        
        # For non-encrypted wallets, set password to None
        if not is_encrypted:
            password = None
        
        # Decrypt wallet to get addresses
        addresses_result = decryptWalletEntries(
            filename=current_wallet,
            password=password,
            totp_code=None,
            address=[],
            fields=['id', 'address'],
            to_json=True
        )
        
        if addresses_result:
            return jsonify({'success': True, 'data': json.loads(addresses_result)})
        else:
            return jsonify({'success': False, 'error': 'Failed to get addresses'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/generate-address')
def generate_address_page():
    """Generate address page"""
    return render_template('generate_address.html', current_wallet=current_wallet)


@app.route('/api/generate-address', methods=['POST'])
def generate_address():
    """Generate new address"""
    try:
        if not current_wallet:
            return jsonify({'success': False, 'error': 'No wallet loaded'})
        
        data = request.json
        password = data.get('password')
        amount = data.get('amount', 1)
        
        # Check if wallet is encrypted
        is_encrypted = wallet_data.get('encrypted', False) if wallet_data else False
        
        # For encrypted wallets, password is required
        if is_encrypted and not password:
            return jsonify({'success': False, 'error': 'Password required for encrypted wallet'})
        
        # For non-encrypted wallets, set password to None
        if not is_encrypted:
            password = None
        
        result = generateAddressHelper(
            filename=current_wallet,
            password=password,
            totp_code=data.get('totp_code'),
            new_wallet=False,
            amount=amount
        )
        
        if result:
            return jsonify({'success': True, 'message': f'Generated {amount} new address(es)!'})
        else:
            return jsonify({'success': False, 'error': 'Failed to generate address'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/paper-wallet')
def paper_wallet_page():
    """Paper wallet page"""
    return render_template('paper_wallet.html', current_wallet=current_wallet)


@app.route('/api/generate-paper-wallet', methods=['POST'])
def generate_paper_wallet():
    """Generate paper wallet"""
    try:
        if not current_wallet:
            return jsonify({'success': False, 'error': 'No wallet loaded'})
        
        data = request.json
        
        result = generatePaperWallet(
            filename=current_wallet,
            password=data.get('password'),
            totp_code=data.get('totp_code'),
            address=data.get('address'),
            private_key=None,
            file_type=data.get('format', 'png').lower()
        )
        
        return jsonify({'success': True, 'message': 'Paper wallet generated successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/settings')
def settings_page():
    """Settings page"""
    return render_template('settings.html')


@app.route('/api/wallet-status')
def get_wallet_status():
    """Get current wallet status"""
    try:
        if not current_wallet:
            return jsonify({'success': False, 'error': 'No wallet loaded'})
        
        is_encrypted = wallet_data.get('encrypted', False) if wallet_data else False
        
        return jsonify({
            'success': True,
            'encrypted': is_encrypted,
            'wallet_path': current_wallet
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("Starting Stellaris Wallet Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
