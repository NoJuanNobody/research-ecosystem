// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 33: Decentralized Storage Pinning Incentives for Collaborative Creative Repositories
/// @notice Perpetual storage endowment model:
///         E(t) = E_0 * (1 + r)^t - \sum_{k=1}^t C_storage(k)
///         Solvency invariant: r * E(t) >= C_storage(t)
contract StoragePinningEscrow {
    struct AssetEndowment {
        string cid;
        uint256 principal;
        uint256 yieldRateBps;
        uint256 periodicStorageCost;
    }

    mapping(bytes32 => AssetEndowment) public endowments;

    event EndowmentCreated(bytes32 indexed assetKey, string cid, uint256 principal);

    function createEndowment(
        string calldata cid,
        uint256 yieldRateBps,
        uint256 periodicStorageCost
    ) external payable returns (bytes32 assetKey) {
        require(msg.value > 0, "Endowment principal required");
        assetKey = keccak256(abi.encodePacked(cid));
        endowments[assetKey] = AssetEndowment({
            cid: cid,
            principal: msg.value,
            yieldRateBps: yieldRateBps,
            periodicStorageCost: periodicStorageCost
        });
        emit EndowmentCreated(assetKey, cid, msg.value);
    }

    function isPerpetuallySolvent(bytes32 assetKey) external view returns (bool) {
        AssetEndowment memory e = endowments[assetKey];
        uint256 periodicYield = (e.principal * e.yieldRateBps) / 10000;
        return periodicYield >= e.periodicStorageCost;
    }
}
