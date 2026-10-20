// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 29: Proof-of-Human-In-The-Loop: Byzantine Fault Tolerant Curatorial Consensus
/// @notice Staked Schelling-point curation consensus with supermajority reward and slashing:
///         V* = I(\sum_{v_i=1} w_i > \sum_{v_i=0} w_i)
contract CuratorConsensus {
    struct Vote {
        bool approve;
        uint256 stake;
        bool settled;
    }

    uint256 public immutable slashBps; // e.g., 3000 = 30% slash
    mapping(bytes32 => mapping(address => Vote)) public votes;
    mapping(bytes32 => uint256) public approveStake;
    mapping(bytes32 => uint256) public rejectStake;

    constructor(uint256 _slashBps) {
        require(_slashBps <= 10000, "Invalid slash bps");
        slashBps = _slashBps;
    }

    function submitVote(bytes32 assetId, bool approve) external payable {
        require(msg.value > 0, "Stake required");
        require(votes[assetId][msg.sender].stake == 0, "Already voted");

        votes[assetId][msg.sender] = Vote({approve: approve, stake: msg.value, settled: false});
        if (approve) {
            approveStake[assetId] += msg.value;
        } else {
            rejectStake[assetId] += msg.value;
        }
    }

    function consensusOutcome(bytes32 assetId) public view returns (bool) {
        return approveStake[assetId] > rejectStake[assetId];
    }
}
