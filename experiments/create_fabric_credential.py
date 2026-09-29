import hashlib
import json
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def canonical_json(data):
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")


# ---------------------------------------
# 1. Create credential
# ---------------------------------------

credential = {
    "credentialId": "CRED003",
    "credentialType": "EducationCredential",
    "issuer": "Alliance University",
    "subjectDid": "did:capstone:USER003",
    "claims": {
        "degree": "M.Tech AI & DS",
        "status": "verified"
    }
}

# ---------------------------------------
# 2. Calculate SHA-256 hash
# ---------------------------------------

payload = canonical_json(credential)

credential_hash = hashlib.sha256(payload).hexdigest()

# ---------------------------------------
# 3. Generate Ed25519 key pair
# ---------------------------------------

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# ---------------------------------------
# 4. Sign credential
# ---------------------------------------

signature = private_key.sign(payload)

signature_b64 = base64.b64encode(signature).decode("utf-8")

public_key_bytes = public_key.public_bytes_raw()
public_key_b64 = base64.b64encode(public_key_bytes).decode("utf-8")

# ---------------------------------------
# 5. Create Fabric-ready record
# ---------------------------------------

fabric_credential = {
    "credentialId": credential["credentialId"],
    "subjectDid": credential["subjectDid"],
    "credentialType": credential["credentialType"],
    "issuer": credential["issuer"],
    "credentialHash": credential_hash,
    "signature": signature_b64,
    "publicKey": public_key_b64
}

# ---------------------------------------
# 6. Save files
# ---------------------------------------

with open("../data/credential_CRED003.json", "w") as f:
    json.dump(credential, f, indent=2)

with open("../data/fabric_credential_CRED003.json", "w") as f:
    json.dump(fabric_credential, f, indent=2)

print("\n=== FABRIC CRYPTOGRAPHIC CREDENTIAL ===")
print(json.dumps(fabric_credential, indent=2))

print("\nCredential saved:")
print("../data/fabric_credential_CRED003.json")
