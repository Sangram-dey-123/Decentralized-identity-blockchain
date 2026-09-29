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


def calculate_hash(data):
    return hashlib.sha256(canonical_json(data)).hexdigest()


# --------------------------------------------------
# 1. Create original digital credential
# --------------------------------------------------

credential = {
    "credentialId": "CRED002",
    "credentialType": "EducationCredential",
    "issuer": "Alliance University",
    "subjectDid": "did:capstone:USER002",
    "claims": {
        "degree": "M.Tech AI & DS",
        "status": "verified"
    }
}

# --------------------------------------------------
# 2. Calculate SHA-256 hash
# --------------------------------------------------

credential_hash = calculate_hash(credential)

print("\n=== ORIGINAL CREDENTIAL ===")
print(json.dumps(credential, indent=2))

print("\nSHA-256 Hash:")
print(credential_hash)

# --------------------------------------------------
# 3. Generate Ed25519 key pair
# --------------------------------------------------

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# --------------------------------------------------
# 4. Create digital signature
# --------------------------------------------------

payload = canonical_json(credential)
signature = private_key.sign(payload)

signature_b64 = base64.b64encode(signature).decode("utf-8")

print("\nEd25519 Signature:")
print(signature_b64)

# --------------------------------------------------
# 5. Verify original credential
# --------------------------------------------------

try:
    public_key.verify(signature, payload)
    original_signature_valid = True
except Exception:
    original_signature_valid = False

recalculated_hash = calculate_hash(credential)
original_hash_valid = recalculated_hash == credential_hash

print("\n=== ORIGINAL VERIFICATION ===")
print("Hash valid:", original_hash_valid)
print("Signature valid:", original_signature_valid)

# --------------------------------------------------
# 6. Tamper with credential
# --------------------------------------------------

tampered_credential = json.loads(json.dumps(credential))

tampered_credential["claims"]["degree"] = "PhD"

print("\n=== TAMPERED CREDENTIAL ===")
print(json.dumps(tampered_credential, indent=2))

# --------------------------------------------------
# 7. Detect hash modification
# --------------------------------------------------

tampered_hash = calculate_hash(tampered_credential)

hash_tampering_detected = tampered_hash != credential_hash

# --------------------------------------------------
# 8. Detect signature modification
# --------------------------------------------------

tampered_payload = canonical_json(tampered_credential)

try:
    public_key.verify(signature, tampered_payload)
    tampered_signature_valid = True
except Exception:
    tampered_signature_valid = False

signature_tampering_detected = not tampered_signature_valid

# --------------------------------------------------
# 9. Display tamper detection result
# --------------------------------------------------

print("\n=== TAMPER DETECTION ===")
print("Original hash:", credential_hash)
print("Tampered hash:", tampered_hash)

print("\nHash tampering detected:", hash_tampering_detected)
print("Signature valid after tampering:", tampered_signature_valid)
print("Signature tampering detected:", signature_tampering_detected)

# --------------------------------------------------
# 10. Objective 2 result
# --------------------------------------------------

objective2_success = (
    original_hash_valid
    and original_signature_valid
    and hash_tampering_detected
    and signature_tampering_detected
)

print("\n=== OBJECTIVE 2 RESULT ===")

if objective2_success:
    print("PASS: Credential authenticity and tampering detection demonstrated.")
else:
    print("FAIL: Cryptographic verification test failed.")
