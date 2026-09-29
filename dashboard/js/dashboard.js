const identities = {

    "USER001": {
        userId: "USER001",
        did: "did:capstone:USER001",
        name: "Sangram Test User",
        sector: "education",
        status: "ACTIVE"
    },

    "USER005": {
        userId: "USER005",
        did: "did:capstone:USER005",
        sector: "healthcare",
        status: "ACTIVE"
    }

};


const credentials = {

    "CRED004": {
        credentialId: "CRED004",
        type: "EducationCredential",
        issuer: "Alliance University",
        hashValid: true,
        signatureValid: true,
        verified: true
    },

    "CRED005": {
        credentialId: "CRED005",
        type: "HealthcareCredential",
        issuer: "City Hospital",
        verified: true
    }

};


const consents = {

    "CONSENT002": {
        consentId: "CONSENT002",
        userId: "USER005",
        verifier: "BANK001",
        credentialId: "CRED005",
        status: "REVOKED",
        notExpired: true,
        valid: false
    }

};


function searchIdentity() {

    const id =
        document.getElementById("userId")
        .value
        .toUpperCase();

    const result =
        document.getElementById("identityResult");

    const identity = identities[id];

    if (!identity) {

        result.innerHTML =
            "<p class='badge red'>IDENTITY NOT FOUND</p>";

        return;
    }

    result.innerHTML = `

        <div class="audit-box">

            <p><b>User ID:</b> ${identity.userId}</p>

            <p><b>DID:</b> ${identity.did}</p>

            <p><b>Name:</b> ${identity.name || "N/A"}</p>

            <p><b>Sector:</b> ${identity.sector}</p>

            <p><b>Status:</b>
                <span class="badge green">
                    ${identity.status}
                </span>
            </p>

        </div>

    `;
}


function verifyCredential() {

    const id =
        document.getElementById("credentialId")
        .value
        .toUpperCase();

    const result =
        document.getElementById("credentialResult");

    const credential = credentials[id];

    if (!credential) {

        result.innerHTML =
            "<p class='badge red'>CREDENTIAL NOT FOUND</p>";

        return;
    }

    result.innerHTML = `

        <div class="audit-box">

            <p><b>Credential:</b>
                ${credential.credentialId}
            </p>

            <p><b>Type:</b>
                ${credential.type}
            </p>

            <p><b>Issuer:</b>
                ${credential.issuer}
            </p>

            <p><b>SHA-256:</b>
                <span class="badge green">
                    ${credential.hashValid ? "VALID" : "INVALID"}
                </span>
            </p>

            <p><b>Ed25519 Signature:</b>
                <span class="badge green">
                    ${credential.signatureValid ? "VALID" : "INVALID"}
                </span>
            </p>

            <p><b>Verification:</b>
                <span class="badge green">
                    ${credential.verified ? "VERIFIED" : "FAILED"}
                </span>
            </p>

        </div>

    `;
}


function checkConsent() {

    const id =
        document.getElementById("consentId")
        .value
        .toUpperCase();

    const result =
        document.getElementById("consentResult");

    const consent = consents[id];

    if (!consent) {

        result.innerHTML =
            "<p class='badge red'>CONSENT NOT FOUND</p>";

        return;
    }

    result.innerHTML = `

        <div class="audit-box">

            <p><b>Consent:</b>
                ${consent.consentId}
            </p>

            <p><b>User:</b>
                ${consent.userId}
            </p>

            <p><b>Verifier:</b>
                ${consent.verifier}
            </p>

            <p><b>Credential:</b>
                ${consent.credentialId}
            </p>

            <p><b>Status:</b>
                <span class="badge red">
                    ${consent.status}
                </span>
            </p>

            <p><b>Not Expired:</b>
                ${consent.notExpired ? "YES" : "NO"}
            </p>

            <p><b>Access:</b>
                <span class="badge red">
                    ${consent.valid ? "ACCEPT" : "REJECT"}
                </span>
            </p>

        </div>

    `;
}
