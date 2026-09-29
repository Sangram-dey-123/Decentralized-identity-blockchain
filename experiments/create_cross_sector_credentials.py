import json
import hashlib
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

BASE = Path("data")
BASE.mkdir(exist_ok=True)

credentials = [
    {
        "credentialId": "CRED005",
        "subjectDid": "did:capstone:USER005",
        "credentialType": "HealthcareCredential",
        "issuer": "City Hospital",
        "claims": {
            "patientStatus": "verified",
            "recordStatus": "active"
        }
    },
    {
        "credentialId": "CRED006",
        "subjectDid": "did:capstone:USER006",
        "credentialType": "BankingCredential",
        "issuer": "Demo Bank",
        "claims": {
            "kycStatus": "verified",
            "accountStatus": "active"
        }
    },
    {
        "credentialId": "CRED007",
        "subjectDid": "did:capstone:USER007",
        "credentialType": "GovernmentCredential",
        "issuer": "Government Authority",
        "claims": {
            "citizenStatus": "verified",
            "documentStatus": "active"
        }
    }
]

for cred in credentials:
    canonical = json.dumps(
        cred,
        sort_keys=True,
        separators=(",", ":")
    )

    digest = hashlib.sha256(canonical.encode()).hexdigest()

    private_key = Ed25519PrivateKey.generate()
    signature = private_key.sign(canonical.encode())

    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    output = {
        **cred,
        "credentialHash": digest,
        "signature": base64.b64encode(signature).decode(),
        "publicKey": public_key,
        "credentialData": canonical
    }

    file_path = BASE / f"{cred['credentialId']}.json"

    with open(file_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nCreated {cred['credentialId']}")
    print(f"Type: {cred['credentialType']}")
    print(f"Issuer: {cred['issuer']}")
    print(f"Hash: {digest}")
    print(f"Saved: {file_path}")

print("\nCross-sector credential generation completed.")
