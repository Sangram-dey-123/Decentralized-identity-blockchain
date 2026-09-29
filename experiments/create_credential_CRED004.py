import json
import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


# =========================================================
# CRED004 — Cryptographically Verifiable Credential
# =========================================================

credential = {
    "credentialId": "CRED004",
    "credentialType": "EducationCredential",
    "issuer": "Alliance University",
    "subjectDid": "did:capstone:USER004",
    "claims": {
        "degree": "M.Tech AI & DS",
        "status": "verified"
    }
}


# =========================================================
# 1. Canonical JSON
# =========================================================

canonical_data = json.dumps(
    credential,
    sort_keys=True,
    separators=(",", ":")
)

print("\n=== CANONICAL CREDENTIAL ===")
print(canonical_data)


# =========================================================
# 2. SHA-256 Hash
# =========================================================

credential_hash = hashlib.sha256(
    canonical_data.encode("utf-8")
).hexdigest()

print("\n=== SHA-256 HASH ===")
print(credential_hash)


# =========================================================
# 3. Generate Ed25519 Key Pair
# =========================================================

private_key = Ed25519PrivateKey.generate()

public_key = private_key.public_key()


# =========================================================
# 4. Export Public Key as PEM
# =========================================================

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

public_key_pem_string = public_key_pem.decode("utf-8")


# =========================================================
# 5. Digital Signature
# =========================================================

signature = private_key.sign(
    canonical_data.encode("utf-8")
)

signature_base64 = base64.b64encode(signature).decode("utf-8")


# =========================================================
# 6. Create Fabric Credential Record
# =========================================================

fabric_credential = {
    "credentialId": credential["credentialId"],
    "subjectDid": credential["subjectDid"],
    "credentialType": credential["credentialType"],
    "issuer": credential["issuer"],
    "credentialHash": credential_hash,
    "signature": signature_base64,
    "publicKey": public_key_pem_string,
    "credentialData": canonical_data
}


# =========================================================
# 7. Save Files
# =========================================================

data_path = "data/credential_CRED004.json"

fabric_path = "data/fabric_credential_CRED004.json"


with open(data_path, "w") as f:
    json.dump(credential, f, indent=4)


with open(fabric_path, "w") as f:
    json.dump(fabric_credential, f, indent=4)


# =========================================================
# 8. Display Result
# =========================================================

print("\n=== CRED004 GENERATED ===")

print("Credential ID:")
print(fabric_credential["credentialId"])

print("\nCredential Hash:")
print(fabric_credential["credentialHash"])

print("\nDigital Signature:")
print(fabric_credential["signature"])

print("\nPublic Key:")
print(fabric_credential["publicKey"])

print("\nCredential Data:")
print(fabric_credential["credentialData"])

print("\nFiles saved:")
print(data_path)
print(fabric_path)
