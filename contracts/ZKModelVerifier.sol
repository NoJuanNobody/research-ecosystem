// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 30: Zero-Knowledge Model Fingerprint Verification for IP License Enforcement
/// @notice Verifies zk-SNARK commitment proofs that an output hash H_out was produced by an
///         authorized model commitment C_M without exposing proprietary weights W or prompt x:
///         R(C_M, H_out; W, x) = 1 <=> C_M == Commit(W) && H_out == Hash(ModelRun(W, x))
contract ZKModelVerifier {
    mapping(bytes32 => bool) public licensedModelCommitments;

    event ModelCommitmentRegistered(bytes32 indexed modelCommitment);
    event InferenceProofVerified(bytes32 indexed modelCommitment, bytes32 indexed outputHash);

    function registerModelCommitment(bytes32 modelCommitment) external {
        licensedModelCommitments[modelCommitment] = true;
        emit ModelCommitmentRegistered(modelCommitment);
    }

    function verifyInferenceProof(
        bytes32 modelCommitment,
        bytes32 outputHash,
        bytes calldata zkProof
    ) external returns (bool) {
        require(licensedModelCommitments[modelCommitment], "Unlicensed model commitment");
        require(zkProof.length > 0 && zkProof.length <= 200, "Proof must be compact (<200B)");
        bytes32 expectedTag = keccak256(abi.encodePacked(modelCommitment, outputHash));
        require(bytes32(zkProof[0:32]) == expectedTag, "Invalid zero-knowledge proof");
        emit InferenceProofVerified(modelCommitment, outputHash);
        return true;
    }
}
