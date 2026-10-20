// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 35: Dynamic Royalty Cascades for Derivative Generative Remix Trees
/// @notice Multi-tier recursive derivative attribution split with decay factor gamma and dust cutoff:
///         R_payout(node) = R_total * \prod_{step \in Path(Root -> node)} (gamma * w_step)
contract RoyaltyCascadeTree {
    struct AssetNode {
        address creator;
        bytes32 parentAsset;
        uint256 decayBps; // gamma in basis points (e.g., 4000 = 40% passed upstream)
    }

    uint256 public immutable dustThresholdWei;
    mapping(bytes32 => AssetNode) public assets;
    mapping(address => uint256) public accruedRoyalties;

    constructor(uint256 _dustThresholdWei) {
        dustThresholdWei = _dustThresholdWei;
    }

    function registerAsset(bytes32 assetId, bytes32 parentAsset, uint256 decayBps) external {
        require(assets[assetId].creator == address(0), "Asset already registered");
        require(decayBps < 10000, "Decay must be < 100%");
        assets[assetId] = AssetNode({creator: msg.sender, parentAsset: parentAsset, decayBps: decayBps});
    }

    function distributeCascade(bytes32 soldAssetId, uint256 saleAmount) external {
        bytes32 current = soldAssetId;
        uint256 remaining = saleAmount;
        uint256 depth = 0;

        while (current != bytes32(0) && remaining >= dustThresholdWei && depth < 16) {
            AssetNode memory node = assets[current];
            if (node.creator == address(0)) break;

            if (node.parentAsset == bytes32(0)) {
                accruedRoyalties[node.creator] += remaining;
                remaining = 0;
                break;
            }

            uint256 upstreamAmount = (remaining * node.decayBps) / 10000;
            if (upstreamAmount < dustThresholdWei) {
                accruedRoyalties[node.creator] += remaining;
                remaining = 0;
                break;
            }

            uint256 directShare = remaining - upstreamAmount;
            accruedRoyalties[node.creator] += directShare;
            remaining = upstreamAmount;
            current = node.parentAsset;
            depth++;
        }
    }
}
