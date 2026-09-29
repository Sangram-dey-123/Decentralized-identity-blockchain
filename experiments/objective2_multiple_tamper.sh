#!/bin/bash

echo "OBJECTIVE 2 - MULTIPLE TAMPER TESTS"
echo "==================================="

echo ""
echo "TEST 1: Original credential"
peer chaincode query \
  -C mychannel \
  -n identity-contract \
  -c '{"function":"CheckCredentialIntegrity","Args":["CRED004","{\"claims\":{\"degree\":\"M.Tech AI & DS\",\"status\":\"verified\"},\"credentialId\":\"CRED004\",\"credentialType\":\"EducationCredential\",\"issuer\":\"Alliance University\",\"subjectDid\":\"did:capstone:USER004\"}"]}'

echo ""
echo "TEST 2: Degree modified"
peer chaincode query \
  -C mychannel \
  -n identity-contract \
  -c '{"function":"CheckCredentialIntegrity","Args":["CRED004","{\"claims\":{\"degree\":\"PhD\",\"status\":\"verified\"},\"credentialId\":\"CRED004\",\"credentialType\":\"EducationCredential\",\"issuer\":\"Alliance University\",\"subjectDid\":\"did:capstone:USER004\"}"]}'

echo ""
echo "TEST 3: Status modified"
peer chaincode query \
  -C mychannel \
  -n identity-contract \
  -c '{"function":"CheckCredentialIntegrity","Args":["CRED004","{\"claims\":{\"degree\":\"M.Tech AI & DS\",\"status\":\"revoked\"},\"credentialId\":\"CRED004\",\"credentialType\":\"EducationCredential\",\"issuer\":\"Alliance University\",\"subjectDid\":\"did:capstone:USER004\"}"]}'

echo ""
echo "TEST 4: Issuer modified"
peer chaincode query \
  -C mychannel \
  -n identity-contract \
  -c '{"function":"CheckCredentialIntegrity","Args":["CRED004","{\"claims\":{\"degree\":\"M.Tech AI & DS\",\"status\":\"verified\"},\"credentialId\":\"CRED004\",\"credentialType\":\"EducationCredential\",\"issuer\":\"Fake University\",\"subjectDid\":\"did:capstone:USER004\"}"]}'

echo ""
echo "TEST 5: Subject DID modified"
peer chaincode query \
  -C mychannel \
  -n identity-contract \
  -c '{"function":"CheckCredentialIntegrity","Args":["CRED004","{\"claims\":{\"degree\":\"M.Tech AI & DS\",\"status\":\"verified\"},\"credentialId\":\"CRED004\",\"credentialType\":\"EducationCredential\",\"issuer\":\"Alliance University\",\"subjectDid\":\"did:capstone:ATTACKER\"}"]}'
