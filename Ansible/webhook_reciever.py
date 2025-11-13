#optional , if you are using splunk enterprise version

#!/usr/bin/env python3
from flask import Flask, request
import subprocess
import json
import re

app = Flask(__name__)

@app.route('/block', methods=['POST'])
def block_ip():
    try:
        # Get data from Splunk
        data = request.get_json(force=True) if request.is_json else {}
        raw_data = request.get_data(as_text=True)
        
        print(f"Received webhook:")
        print(f"JSON data: {data}")
        print(f"Raw data: {raw_data}")
        
        # Try to extract IP from multiple formats
        ip = None
        
        # Format 1: {"result": {"Attacking IP": "x.x.x.x"}}
        if 'result' in data:
            ip = data['result'].get('Attacking IP')
        
        # Format 2: {"Attacking IP": "x.x.x.x"}
        if not ip:
            ip = data.get('Attacking IP')
        
        # Format 3: Extract from raw text
        if not ip and raw_data:
            match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', raw_data)
            if match:
                ip = match.group(1)
        
        print(f"Extracted IP: {ip}")
        
        # Skip test IPs
        if ip and ip not in ['1.2.3.4', '5.6.7.8', '127.0.0.1']:
            print(f"Blocking IP: {ip}")
            
            # Run Ansible playbook
            result = subprocess.run([
                'ansible-playbook',
                '/home/twesha/splunk-ids-project/playbooks/block_attacker.yml',
                '-e', f'ip_to_block={ip}'
            ], capture_output=True, text=True)
            
            print(f"Ansible stdout: {result.stdout}")
            print(f"Ansible stderr: {result.stderr}")
            
            if result.returncode == 0:
                return f"Successfully blocked {ip}", 200
            else:
                return f"Failed to block {ip}: {result.stderr}", 500
        else:
            return f"Invalid or test IP: {ip}", 400
            
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
