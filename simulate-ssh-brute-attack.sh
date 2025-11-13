#!/bin/bash

CLIENT1="ip-1"
CLIENT2="ip-2"

USERNAMES=("admin" "root" "user" "test" "guest" "oracle" "postgres" "mysql" "Administrator" "support" "backup" "operator" "hacker" "attacker" "wronguser" "badactor")

echo "\U0001f534 Simulating brute-force attack..."

for USER in "${USERNAMES[@]}"; do
    echo "Attempting: $USER@$CLIENT1"
    timeout 2 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$CLIENT1 2>/dev/null || true
    sleep 0.5
done

echo ""
echo "Switching to Client 2..."
echo ""

for USER in "${USERNAMES[@]}"; do
    echo "Attempting: $USER@$CLIENT2"
    timeout 2 ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$CLIENT2 2>/dev/null || true
    sleep 0.5
done

echo ""
echo "\u2705 Attack simulation complete!"
echo "\U0001f550 Wait 60 seconds, then check Splunk:"
echo "   Search: index=ssh_logs sourcetype=linux_secure \"Failed password\""
