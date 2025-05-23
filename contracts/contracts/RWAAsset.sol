// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract RWAAsset {
    enum AssetStatus { Issued, Active, Delinquent, Settled }

    struct Asset {
        address issuer;
        address owner;
        string metadataURI;
        uint256 riskScore;
        uint256 value;
        AssetStatus status;
    }

    uint256 public assetCount;
    mapping(uint256 => Asset) public assets;

    event AssetIssued(uint256 indexed assetId, address indexed issuer, address owner);
    event RiskScoreUpdated(uint256 indexed assetId, uint256 newRiskScore);
    event StatusUpdated(uint256 indexed assetId, AssetStatus newStatus);

    function issueAsset(address _owner, string memory _uri, uint256 _value) external returns (uint256) {
        assets[assetCount] = Asset(msg.sender, _owner, _uri, 0, _value, AssetStatus.Issued);
        emit AssetIssued(assetCount, msg.sender, _owner);
        return assetCount++;
    }

    function updateRiskScore(uint256 _assetId, uint256 _score) external {
        require(msg.sender == assets[_assetId].issuer, "Only issuer can update risk");
        assets[_assetId].riskScore = _score;
        emit RiskScoreUpdated(_assetId, _score);
    }

    function updateStatus(uint256 _assetId, AssetStatus _status) external {
        require(msg.sender == assets[_assetId].issuer, "Only issuer can update status");
        assets[_assetId].status = _status;
        emit StatusUpdated(_assetId, _status);
    }
}
