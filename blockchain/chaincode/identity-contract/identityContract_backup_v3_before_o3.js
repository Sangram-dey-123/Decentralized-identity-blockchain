'use strict';

const { Contract } = require('fabric-contract-api');
const crypto = require('crypto');

class IdentityContract extends Contract {

    // =========================================================
    // OBJECTIVE 1 — IDENTITY MANAGEMENT
    // =========================================================

    async IdentityExists(ctx, userId) {

        const data = await ctx.stub.getState(userId);

        return data && data.length > 0;
    }

    async RegisterIdentity(
        ctx,
        userId,
        name,
        sector,
        publicKey
    ) {

        if (!userId || !name || !sector || !publicKey) {
            throw new Error(
                'userId, name, sector and publicKey are required'
            );
        }

        const exists = await this.IdentityExists(ctx, userId);

        if (exists) {
            throw new Error(
                `Identity ${userId} already exists`
            );
        }

        const timestamp = ctx.stub.getTxTimestamp();

        const createdAt = new Date(
            Number(timestamp.seconds) * 1000
        ).toISOString();

        const identity = {
            userId: userId,
            did: `did:capstone:${userId}`,
            name: name,
            sector: sector,
            publicKey: publicKey,
            status: 'ACTIVE',
            createdAt: createdAt
        };

        await ctx.stub.putState(
            userId,
            Buffer.from(JSON.stringify(identity))
        );

        await this.CreateAuditEvent(
            ctx,
            userId,
            'IDENTITY_REGISTERED',
            `Identity registered for ${userId}`
        );

        return JSON.stringify(identity);
    }

    async ReadIdentity(ctx, userId) {

        const data = await ctx.stub.getState(userId);

        if (!data || data.length === 0) {
            throw new Error(
                `Identity ${userId} does not exist`
            );
        }

        return data.toString();
    }


    // =========================================================
    // OBJECTIVE 2 — CRYPTOGRAPHIC CREDENTIAL MANAGEMENT
    // =========================================================

    async CredentialExists(ctx, credentialId) {

        const data = await ctx.stub.getState(credentialId);

        return data && data.length > 0;
    }


    /*
     * RegisterCredential
     *
     * Stores:
     * - SHA-256 credential hash
     * - Ed25519 digital signature
     * - Ed25519 public key
     * - Exact canonical credential data
     *
     * The credentialData is required so that the chaincode
     * can independently calculate the SHA-256 hash and verify
     * the digital signature.
     */

    async RegisterCredential(
        ctx,
        credentialId,
        subjectDid,
        credentialType,
        issuer,
        credentialHash,
        signature,
        publicKey,
        credentialData
    ) {

        if (
            !credentialId ||
            !subjectDid ||
            !credentialType ||
            !issuer ||
            !credentialHash ||
            !signature ||
            !publicKey ||
            !credentialData
        ) {
            throw new Error(
                'All credential fields including credentialData are required'
            );
        }

        const existing = await ctx.stub.getState(
            credentialId
        );

        if (existing && existing.length > 0) {
            throw new Error(
                `Credential ${credentialId} already exists`
            );
        }

        // Validate that credentialData is valid JSON
        try {
            JSON.parse(credentialData);
        } catch (error) {
            throw new Error(
                'credentialData must be valid JSON'
            );
        }

        const timestamp = ctx.stub.getTxTimestamp();

        const registeredAt = new Date(
            Number(timestamp.seconds) * 1000
        ).toISOString();

        const credential = {
            credentialId: credentialId,
            subjectDid: subjectDid,
            credentialType: credentialType,
            issuer: issuer,
            credentialHash: credentialHash,
            signature: signature,
            publicKey: publicKey,
            credentialData: credentialData,
            status: 'REGISTERED',
            registeredAt: registeredAt
        };

        await ctx.stub.putState(
            credentialId,
            Buffer.from(JSON.stringify(credential))
        );

        await this.CreateAuditEvent(
            ctx,
            subjectDid,
            'CREDENTIAL_REGISTERED',
            `Credential ${credentialId} registered`
        );

        return JSON.stringify(credential);
    }


    async IssueCredential(ctx, credentialId) {

        const exists = await this.CredentialExists(
            ctx,
            credentialId
        );

        if (!exists) {
            throw new Error(
                `Credential ${credentialId} does not exist`
            );
        }

        const data = await ctx.stub.getState(
            credentialId
        );

        const credential = JSON.parse(
            data.toString()
        );

        if (credential.status === 'ISSUED') {
            throw new Error(
                `Credential ${credentialId} is already issued`
            );
        }

        const timestamp = ctx.stub.getTxTimestamp();

        const issuedAt = new Date(
            Number(timestamp.seconds) * 1000
        ).toISOString();

        credential.status = 'ISSUED';
        credential.issuedAt = issuedAt;

        await ctx.stub.putState(
            credentialId,
            Buffer.from(JSON.stringify(credential))
        );

        await this.CreateAuditEvent(
            ctx,
            credential.subjectDid,
            'CREDENTIAL_ISSUED',
            `Credential ${credentialId} issued`
        );

        return JSON.stringify(credential);
    }


    async ReadCredential(ctx, credentialId) {

        const data = await ctx.stub.getState(
            credentialId
        );

        if (!data || data.length === 0) {
            throw new Error(
                `Credential ${credentialId} does not exist`
            );
        }

        return data.toString();
    }


    // =========================================================
    // SHA-256 + ED25519 VERIFICATION
    // =========================================================

    async VerifyCredential(ctx, credentialId) {

        const exists = await this.CredentialExists(
            ctx,
            credentialId
        );

        if (!exists) {
            throw new Error(
                `Credential ${credentialId} does not exist`
            );
        }

        const data = await ctx.stub.getState(
            credentialId
        );

        const credential = JSON.parse(
            data.toString()
        );

        if (!credential.credentialData) {

            throw new Error(
                `Credential ${credentialId} does not contain credentialData`
            );
        }

        if (!credential.publicKey) {

            throw new Error(
                `Credential ${credentialId} does not contain publicKey`
            );
        }

        // -----------------------------------------------------
        // 1. Calculate SHA-256 from stored credentialData
        // -----------------------------------------------------

        const calculatedHash = crypto
            .createHash('sha256')
            .update(
                credential.credentialData,
                'utf8'
            )
            .digest('hex');

        const hashValid =
            calculatedHash === credential.credentialHash;


        // -----------------------------------------------------
        // 2. Verify Ed25519 digital signature
        // -----------------------------------------------------

        let signatureValid = false;

        try {

            const publicKeyObject =
                crypto.createPublicKey(
                    credential.publicKey
                );

            const signatureBuffer =
                Buffer.from(
                    credential.signature,
                    'base64'
                );

            signatureValid =
                crypto.verify(
                    null,
                    Buffer.from(
                        credential.credentialData,
                        'utf8'
                    ),
                    publicKeyObject,
                    signatureBuffer
                );

        } catch (error) {

            signatureValid = false;
        }


        // -----------------------------------------------------
        // 3. Final verification decision
        // -----------------------------------------------------

        const verified =
            credential.status === 'ISSUED' &&
            hashValid &&
            signatureValid;


        const result = {

            credentialId:
                credential.credentialId,

            subjectDid:
                credential.subjectDid,

            credentialType:
                credential.credentialType,

            issuer:
                credential.issuer,

            status:
                credential.status,

            storedHash:
                credential.credentialHash,

            calculatedHash:
                calculatedHash,

            hashValid:
                hashValid,

            signatureValid:
                signatureValid,

            verified:
                verified
        };


        await this.CreateAuditEvent(
            ctx,
            credential.subjectDid,
            'CREDENTIAL_CRYPTOGRAPHICALLY_VERIFIED',
            `Credential ${credentialId} cryptographic verification requested`
        );

        return JSON.stringify(result);
    }


    /*
     * CheckCredentialIntegrity
     *
     * Used for tamper-detection experiments.
     *
     * The supplied credentialData is compared against:
     * - stored SHA-256 hash
     * - stored Ed25519 signature
     * - stored public key
     */

    async CheckCredentialIntegrity(
        ctx,
        credentialId,
        suppliedCredentialData
    ) {

        const exists = await this.CredentialExists(
            ctx,
            credentialId
        );

        if (!exists) {
            throw new Error(
                `Credential ${credentialId} does not exist`
            );
        }

        if (!suppliedCredentialData) {
            throw new Error(
                'suppliedCredentialData is required'
            );
        }

        const data = await ctx.stub.getState(
            credentialId
        );

        const credential = JSON.parse(
            data.toString()
        );


        // -----------------------------------------------------
        // Calculate hash of supplied data
        // -----------------------------------------------------

        const calculatedHash = crypto
            .createHash('sha256')
            .update(
                suppliedCredentialData,
                'utf8'
            )
            .digest('hex');


        const hashValid =
            calculatedHash === credential.credentialHash;


        // -----------------------------------------------------
        // Verify supplied data against original signature
        // -----------------------------------------------------

        let signatureValid = false;

        try {

            const publicKeyObject =
                crypto.createPublicKey(
                    credential.publicKey
                );

            const signatureBuffer =
                Buffer.from(
                    credential.signature,
                    'base64'
                );

            signatureValid =
                crypto.verify(
                    null,
                    Buffer.from(
                        suppliedCredentialData,
                        'utf8'
                    ),
                    publicKeyObject,
                    signatureBuffer
                );

        } catch (error) {

            signatureValid = false;
        }


        const integrityValid =
            hashValid &&
            signatureValid;


        const result = {

            credentialId:
                credential.credentialId,

            originalHash:
                credential.credentialHash,

            calculatedHash:
                calculatedHash,

            hashValid:
                hashValid,

            signatureValid:
                signatureValid,

            integrityValid:
                integrityValid
        };


        await this.CreateAuditEvent(
            ctx,
            credential.subjectDid,
            'CREDENTIAL_INTEGRITY_CHECKED',
            `Credential ${credentialId} integrity check performed`
        );

        return JSON.stringify(result);
    }


    // =========================================================
    // AUDIT TRAIL
    // =========================================================

    async CreateAuditEvent(
        ctx,
        subjectId,
        eventType,
        description
    ) {

        const txId = ctx.stub.getTxID();

        const timestamp = ctx.stub.getTxTimestamp();

        const timestampISO = new Date(
            Number(timestamp.seconds) * 1000
        ).toISOString();

        const auditId =
            `AUDIT_${txId}`;

        const auditEvent = {

            auditId:
                auditId,

            subjectId:
                subjectId,

            eventType:
                eventType,

            description:
                description,

            transactionId:
                txId,

            timestamp:
                timestampISO
        };

        await ctx.stub.putState(
            auditId,
            Buffer.from(
                JSON.stringify(auditEvent)
            )
        );

        return JSON.stringify(auditEvent);
    }


    async GetAuditHistory(
        ctx,
        subjectId
    ) {

        const iterator =
            await ctx.stub.getStateByRange(
                'AUDIT_',
                'AUDIT_\uffff'
            );

        const results = [];

        let result =
            await iterator.next();

        while (!result.done) {

            const value =
                result.value.value.toString();

            try {

                const auditEvent =
                    JSON.parse(value);

                if (
                    auditEvent.subjectId === subjectId
                ) {
                    results.push(
                        auditEvent
                    );
                }

            } catch (error) {

                // Ignore invalid audit records
            }

            result =
                await iterator.next();
        }

        await iterator.close();

        return JSON.stringify(results);
    }
}

module.exports = IdentityContract;
