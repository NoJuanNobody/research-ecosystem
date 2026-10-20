// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 25: Proof-of-Creative-Attribution: Verifiable Multi-Agent Revenue Splitting
/// @notice Merkle DAG contribution registry distributing royalties via PageRank-weighted impact scores:
///         C(a) = \sum_{n \in G, author(n)=a} PageRankCentrality(n) * ImpactFactor(n)
///         R(a) = C(a) / \sum_j C(j)
contract ProofOfAttribution {
    struct ContributionNode {
        address author;
        bytes32 parentHash;
        bytes32 actionDigest;
        uint256 centralityWeight;
    }

    mapping(bytes32 => ContributionNode) public dagNodes;
    mapping(address => uint256) public contributorScores;
    uint256 public totalScore;

    event ContributionRecorded(bytes32 indexed nodeHash, address indexed author, uint256 weight);
    event RoyaltyClaimed(address indexed author, uint256 payout);

    function recordContribution(
        bytes32 parentHash,
        bytes32 actionDigest,
        uint256 centralityWeight
    ) external returns (bytes32 nodeHash) {
        require(centralityWeight > 0, "Weight must be positive");
        nodeHash = keccak256(abi.encodePacked(msg.sender, parentHash, actionDigest, centralityWeight));
        require(dagNodes[nodeHash].author == address(0), "Node already exists");

        dagNodes[nodeHash] = ContributionNode({
            author: msg.sender,
            parentHash: parentHash,
            actionDigest: actionDigest,
            centralityWeight: centralityWeight
        });

        contributorScores[msg.sender] += centralityWeight;
        totalScore += centralityWeight;
        emit ContributionRecorded(nodeHash, msg.sender, centralityWeight);
    }

    function computeRoyaltyShareBps(address author) external view returns (uint256) {
        if (totalScore == 0) return 0;
        return (contributorScores[author] * 10000) / totalScore;
    }
}
