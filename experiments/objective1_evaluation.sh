#!/bin/bash

set -e

TEST_NETWORK="$HOME/fabric/fabric-samples/test-network"
CHANNEL="mychannel"
CC_NAME="identity-contract"

export PATH="$HOME/fabric/bin:$PATH"
export FABRIC_CFG_PATH="$HOME/fabric/config"

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH="$TEST_NETWORK/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"
export CORE_PEER_ADDRESS="localhost:7051"
export CORE_PEER_TLS_ROOTCERT_FILE="$TEST_NETWORK/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"

echo "=== OBJECTIVE 1 — FABRIC FUNCTIONAL EVALUATION ==="

USER_ID="O1USER001"
CRED_ID="O1CRED001"

echo ""
echo "1. Register Identity"
time peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "$TEST_NETWORK/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C "$CHANNEL" \
  -n "$CC_NAME" \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "$TEST_NETWORK/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  -c "{\"function\":\"RegisterIdentity\",\"Args\":[\"$USER_ID\",\"O1 Test User\",\"education\",\"O1_PUBLIC_KEY\"]}"

echo ""
echo "2. Read Identity"
time peer chaincode query \
  -C "$CHANNEL" \
  -n "$CC_NAME" \
  -c "{\"function\":\"ReadIdentity\",\"Args\":[\"$USER_ID\"]}"

echo ""
echo "3. Register Credential"

CREDENTIAL_DATA='{\"credentialId\":\"O1CRED001\",\"credentialType\":\"EducationCredential\",\"issuer\":\"Alliance University\",\"subjectDid\":\"did:capstone:O1USER001\",\"claims\":{\"degree\":\"M.Tech AI & DS\",\"status\":\"verified\"}}'

CREDENTIAL_HASH=$(python -c "import hashlib; print(hashlib.sha256('$CREDENTIAL_DATA'.encode()).hexdigest())")

echo "Credential hash: $CREDENTIAL_HASH"

peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "$TEST_NETWORK/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C "$CHANNEL" \
  -n "$CC_NAME" \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "$TEST_NETWORK/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  -c "{\"function\":\"RegisterCredential\",\"Args\":[\"$CRED_ID\",\"did:capstone:$USER_ID\",\"EducationCredential\",\"Alliance University\",\"$CREDENTIAL_HASH\",\"O1_SIGNATURE\",\"O1_PUBLIC_KEY\",\"$CREDENTIAL_DATA\"]}"

echo ""
echo "4. Issue Credential"
time peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "$TEST_NETWORK/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C "$CHANNEL" \
  -n "$CC_NAME" \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "$TEST_NETWORK/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  -c "{\"function\":\"IssueCredential\",\"Args\":[\"$CRED_ID\"]}"

echo ""
echo "5. Read Credential"
time peer chaincode query \
  -C "$CHANNEL" \
  -n "$CC_NAME" \
  -c "{\"function\":\"ReadCredential\",\"Args\":[\"$CRED_ID\"]}"

echo ""
echo "=== OBJECTIVE 1 EVALUATION COMPLETED ==="
