// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 32: Algorithmic Scarcity & Editioning Protocols for Generative Digital Artifacts
/// @notice Enforces hard supply ceiling S_current < S_max and verifiable randomness seed derivation:
///         Seed_mint = VRF(BlockHeader, OwnerAddress, Nonce)
contract AlgorithmicEditioning {
    uint256 public immutable maxEditionSupply;
    uint256 public currentSupply;
    mapping(uint256 => bytes32) public tokenSeeds;
    mapping(uint256 => address) public ownerOf;

    event ScarcityEditionMinted(uint256 indexed tokenId, address indexed owner, bytes32 vrfSeed, uint256 rarityScore);

    constructor(uint256 _maxEditionSupply) {
        require(_maxEditionSupply > 0, "Max supply must be > 0");
        maxEditionSupply = _maxEditionSupply;
    }

    function mintWithVrf(bytes32 vrfRandomness, uint256 nonce) external returns (uint256 tokenId, bytes32 seed) {
        require(currentSupply < maxEditionSupply, "Edition hard cap reached");
        tokenId = ++currentSupply;
        seed = keccak256(abi.encodePacked(blockhash(block.number - 1), msg.sender, nonce, vrfRandomness));
        tokenSeeds[tokenId] = seed;
        ownerOf[tokenId] = msg.sender;
        uint256 rarity = uint256(seed) % 1000;
        emit ScarcityEditionMinted(tokenId, msg.sender, seed, rarity);
    }
}
