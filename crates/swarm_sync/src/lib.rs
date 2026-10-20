//! Paper 27: Decentralized Bandwidth Allocation for Edge Diffusion Swarms
//!
//! Tit-for-tat peering priority score between node $i$ and node $j$:
//! $\gamma_{ij} = \frac{\text{UploadRate}(j \to i)}{\sum_k \text{UploadRate}(k \to i)} \cdot (1 + \delta_{latency}(i, j))$

use std::collections::BTreeMap;

#[derive(Debug, Clone)]
pub struct BitswapCreditLedger {
    pub upload_rates: BTreeMap<String, f64>,
    pub latency_bonuses: BTreeMap<String, f64>,
}

impl BitswapCreditLedger {
    pub fn new() -> Self {
        Self {
            upload_rates: BTreeMap::new(),
            latency_bonuses: BTreeMap::new(),
        }
    }

    pub fn record_peer_stats(&mut self, peer_id: &str, upload_mbps: f64, latency_bonus: f64) {
        self.upload_rates.insert(peer_id.to_string(), upload_mbps.max(0.0));
        self.latency_bonuses.insert(peer_id.to_string(), latency_bonus);
    }

    pub fn priority_score(&self, peer_id: &str) -> f64 {
        let total: f64 = self.upload_rates.values().sum();
        if total <= 0.0 {
            return 0.0;
        }
        let rate = self.upload_rates.get(peer_id).copied().unwrap_or(0.0);
        let delta = self.latency_bonuses.get(peer_id).copied().unwrap_or(0.0);
        (rate / total) * (1.0 + delta)
    }

    pub fn rank_peers(&self) -> Vec<(String, f64)> {
        let mut ranked: Vec<(String, f64)> = self
            .upload_rates
            .keys()
            .map(|p| (p.clone(), self.priority_score(p)))
            .collect();
        ranked.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        ranked
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tit_for_tat_priority() {
        let mut ledger = BitswapCreditLedger::new();
        ledger.record_peer_stats("peer_fast", 80.0, 0.25);
        ledger.record_peer_stats("peer_slow", 20.0, 0.05);
        let ranked = ledger.rank_peers();
        assert_eq!(ranked[0].0, "peer_fast");
        assert!((ranked[0].1 - 1.0).abs() < 1e-6);
    }
}
