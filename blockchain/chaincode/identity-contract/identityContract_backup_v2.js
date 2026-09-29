'use strict';

const { Contract } = require('fabric-contract-api');

class IdentityContract extends Contract {

    // =========================================================
    // OBJECTIVE 1 — IDENTITY MANAGEMENT
    // =========================================================

    async IdentityExists(ctx, userId) {
        const data = await ctx.stub.getState(userId);
        return data && data.length > 0;
    }

    async RegisterIdentity(ctx, userId, name, sector, publicKey) {

        if (!userId || !name || !sector || !publicKey) {
            throw new Error(
                'userId, name, sector and publicKey are required'
            );
        }

        const exists = await this.IdentityExists(ctx, userId);

        if (exists) {
            throw new Error(`Identity ${userId} already exists`);
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
    // OBJECTIVE 2 — CREDENTIAL MANAGEMENT
    // =========================================================

    async CredentialExists(ctx, credentialId) {

        const data = await ctx.stub.getState(credentialId);

        return data && data.length > 0;
    }


    /*
     * RegisterCredential
     *
     * New field:
     * publicKey
     *
     * This public key will later be used for
     * Ed25519 signature verification.
     */

    async RegisterCredential(
        ctx,
        credentialId,
        subjectDid,
        credentialType,
        issuer,
        credentialHash,
        signature,
        publicKey
    ) {

        if (
            !credentialId ||
            !subjectDid ||
            !credentialType ||
            !issuer ||
            !credentialHash ||
            !signature ||
            !publicKey
        ) {
            throw new Error(
                'All credential fields including publicKey are required'
            );
        }

        const existing = await ctx.stub.getState(credentialId);

        if (existing && existing.length > 0) {
            throw new Error(
                `Credential ${credentialId} already exists`
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

        const data = await ctx.stub.getState(credentialId);

        const credential = JSON.parse(data.toString());

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

        const data = await ctx.stub.getState(credentialId);

        if (!data || data.length === 0) {
            throw new Error(
                `Credential ${credentialId} does not exist`
            );
        }

        return data.toString();
    }


    /*
     * Current verification function.
     *
     * IMPORTANT:
     * This function currently checks the Fabric credential
     * status only.
     *
     * The actual SHA-256 + Ed25519 cryptographic verification
     * will be added in the next step.
     */

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

        const data = await ctx.stub.getState(credentialId);

        const credential = JSON.parse(data.toString());

        const verified =
            credential.status === 'ISSUED';

        const result = {
            credentialId: credential.credentialId,
            subjectDid: credential.subjectDid,
            credentialType: credential.credentialType,
            issuer: credential.issuer,
            status: credential.status,
            credentialHash: credential.credentialHash,
            signature: credential.signature,
            publicKey: credential.publicKey,
            verified: verified
        };

        await this.CreateAuditEvent(
            ctx,
            credential.subjectDid,
            'CREDENTIAL_VERIFIED',
            `Credential ${credentialId} verification requested`
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

        const auditId = `AUDIT_${txId}`;

        const auditEvent = {
            auditId: auditId,
            subjectId: subjectId,
            eventType: eventType,
            description: description,
            transactionId: txId,
            timestamp: timestampISO
        };

        await ctx.stub.putState(
            auditId,
            Buffer.from(JSON.stringify(auditEvent))
        );

        return JSON.stringify(auditEvent);
    }


    async GetAuditHistory(ctx, subjectId) {

        const iterator = await ctx.stub.getStateByRange(
            'AUDIT_',
            'AUDIT_\uffff'
        );

        const results = [];

        let result = await iterator.next();

        while (!result.done) {

            const value = result.value.value.toString();

            try {

                const auditEvent = JSON.parse(value);

                if (auditEvent.subjectId === subjectId) {
                    results.push(auditEvent);
                }

            } catch (error) {

                // Ignore invalid audit records

            }

            result = await iterator.next();
        }

        await iterator.close();

        return JSON.stringify(results);
    }
}


module.exports = IdentityContract;
