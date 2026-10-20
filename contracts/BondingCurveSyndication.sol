// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Paper 26: Dynamic Bonding Curves for Algorithmic Content Syndication
/// @notice Bancor-style power bonding curve P(S) = k * S^alpha with reserve integral:
///         R(S) = (k / (alpha + 1)) * S^(alpha + 1)
contract BondingCurveSyndication {
    uint256 public immutable kCoeff;
    uint256 public immutable alphaExponent; // integer exponent >= 1
    uint256 public totalSupply;
    uint256 public reserveBalance;
    mapping(address => uint256) public balanceOf;

    event EditionMinted(address indexed buyer, uint256 amount, uint256 reserveAdded);
    event EditionBurned(address indexed seller, uint256 amount, uint256 reserveReturned);

    constructor(uint256 _kCoeff, uint256 _alphaExponent) {
        require(_kCoeff > 0 && _alphaExponent >= 1, "Invalid curve parameters");
        kCoeff = _kCoeff;
        alphaExponent = _alphaExponent;
    }

    function requiredReserveForSupply(uint256 supply) public view returns (uint256) {
        return (kCoeff * (supply ** (alphaExponent + 1))) / (alphaExponent + 1);
    }

    function quoteMintCost(uint256 amount) public view returns (uint256) {
        uint256 nextSupply = totalSupply + amount;
        return requiredReserveForSupply(nextSupply) - requiredReserveForSupply(totalSupply);
    }

    function mint(uint256 amount) external payable {
        uint256 cost = quoteMintCost(amount);
        require(msg.value >= cost, "Insufficient reserve deposit");
        totalSupply += amount;
        reserveBalance += cost;
        balanceOf[msg.sender] += amount;
        emit EditionMinted(msg.sender, amount, cost);
    }
}
