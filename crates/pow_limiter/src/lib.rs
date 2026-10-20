//! Paper 34: Network-Decentralized Rate Limiting & Anti-Sybil Proof-of-Compute
//!
//! Dynamic difficulty adjustment based on inbound request pressure $\lambda$:
//! $D(t+1) = D(t) \cdot (1 + \kappa (\frac{\lambda_{current}}{\lambda_{target}} - 1))$

pub struct AntiSybilPowLimiter {
    pub difficulty: f64,
    pub kappa: f64,
    pub target_rate: f64,
}

impl AntiSybilPowLimiter {
    pub fn new(initial_difficulty: f64, kappa: f64, target_rate: f64) -> Self {
        Self {
            difficulty: initial_difficulty.max(1.0),
            kappa,
            target_rate: target_rate.max(1.0),
        }
    }

    pub fn update_difficulty(&mut self, current_rate: f64) -> f64 {
        let factor = 1.0 + self.kappa * ((current_rate / self.target_rate) - 1.0);
        self.difficulty = (self.difficulty * factor).max(1.0);
        self.difficulty
    }

    pub fn compute_digest(client: &str, timestamp: u64, endpoint: &str, nonce: u64) -> u64 {
        let mut h: u64 = 0xcbf29ce484222325;
        for &b in client.as_bytes().iter().chain(endpoint.as_bytes().iter()) {
            h ^= b as u64;
            h = h.wrapping_mul(0x100000001b3);
        }
        h ^= timestamp.wrapping_mul(0x9E3779B97F4A7C15);
        h ^= nonce.wrapping_mul(0xBF58476D1CE4E5B9);
        h = (h ^ (h >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        h = (h ^ (h >> 27)).wrapping_mul(0x94d049bb133111eb);
        h ^ (h >> 31)
    }

    pub fn target_ceiling(&self) -> u64 {
        (u64::MAX as f64 / self.difficulty) as u64
    }

    pub fn verify_nonce(&self, client: &str, timestamp: u64, endpoint: &str, nonce: u64) -> bool {
        Self::compute_digest(client, timestamp, endpoint, nonce) < self.target_ceiling()
    }

    pub fn solve_nonce(&self, client: &str, timestamp: u64, endpoint: &str) -> u64 {
        let ceiling = self.target_ceiling();
        for nonce in 0..u64::MAX {
            if Self::compute_digest(client, timestamp, endpoint, nonce) < ceiling {
                return nonce;
            }
        }
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pow_solve_verify_and_dynamic_difficulty() {
        let mut limiter = AntiSybilPowLimiter::new(16.0, 0.5, 100.0);
        let nonce = limiter.solve_nonce("0xAgent1", 1700000000, "/v1/infer");
        assert!(limiter.verify_nonce("0xAgent1", 1700000000, "/v1/infer", nonce));
        let d_next = limiter.update_difficulty(300.0);
        assert!(d_next > 16.0);
    }
}
