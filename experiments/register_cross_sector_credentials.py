import json
import subprocess
import sys
from pathlib import Path

BASE = Path.home() / "decentralized-identity-blockchain"
FABRIC_BIN = Path.home() / "fabric" / "bin"

ENV = {
    **__import__("os").environ,
    "PATH": f"{FABRIC_BIN}:{__import__('os').environ.get('PATH', '')}",
}

def register(cid):
    file_path = BASE / "data" / f"{cid}.json"

    with open(file_path) as f:
        c = json.load(f)

    args = [
        "peer", "chaincode", "invoke",
        "-o", "localhost:7050",
        "--ordererTLSHostnameOverride", "orderer.example.com",
        "--tls",
        "--cafile", str(
            Path.home() / "fabric/fabric-samples/test-network/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem"
        ),
        "-C", "mychannel",
        "-n", "identity-contract",
        "--peerAddresses", "localhost:7051",
        "--tlsRootCertFiles", str(
            Path.home() / "fabric/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
        ),
        "--peerAddresses", "localhost:9051",
        "--tlsRootCertFiles", str(
            Path.home() / "fabric/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
        ),
        "-c",
        json.dumps({
            "function": "RegisterCredential",
            "Args": [
                c["credentialId"],
                c["subjectDid"],
                c["credentialType"],
                c["issuer"],
                c["credentialHash"],
                c["signature"],
                c["publicKey"],
                c["credentialData"]
            ]
        })
    ]

    print(f"\nRegistering {cid}...")
    result = subprocess.run(args, env=ENV, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode == 0:
        print(f"SUCCESS: {cid} registration submitted.")
    else:
        print(f"FAILED: {cid}")
        sys.exit(result.returncode)


for cid in ["CRED005"]:
    register(cid)

print("\nCross-sector credential registration completed.")
