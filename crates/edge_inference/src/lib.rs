//! Paper 01: Sub-4-Bit Speculative Streaming on Edge Silicon (Zero-DRAM Offloading)
//!
//! Implements speculative decoding pairing a ternary 1.58-bit draft model on dedicated NPU SRAM
//! with an INT4 target model in unified RAM:
//! $\alpha = \min(1, P_{target}(x_{t+k}) / P_{draft}(x_{t+k}))$

#[derive(Debug, Clone)]
pub struct SpeculativeStreamerConfig {
    pub target_model_path: String,
    pub draft_model_path: String,
    pub lookahead_k: u32,
    pub temperature: f32,
}

impl Default for SpeculativeStreamerConfig {
    fn default() -> Self {
        Self {
            target_model_path: "models/target_int4.gguf".to_string(),
            draft_model_path: "models/draft_1_58bit.tqtensor".to_string(),
            lookahead_k: 5,
            temperature: 0.2,
        }
    }
}

pub struct SpeculativeStreamer {
    pub config: SpeculativeStreamerConfig,
}

impl SpeculativeStreamer {
    pub fn new(config: SpeculativeStreamerConfig) -> Self {
        Self { config }
    }

    /// Computes modified speculative rejection sampling acceptance probability:
    /// $\alpha = \min(1, P_{target}(x) / P_{draft}(x))$
    pub fn acceptance_probability(p_target: f32, p_draft: f32) -> f32 {
        if p_draft <= 0.0 {
            return if p_target > 0.0 { 1.0 } else { 0.0 };
        }
        (p_target / p_draft).min(1.0).max(0.0)
    }

    /// Verifies a speculative lookahead batch of K draft tokens against target probabilities.
    /// Returns accepted prefix tokens plus one residual token if rejected early.
    pub fn verify_speculative_step(
        &self,
        draft_tokens: &[u32],
        p_draft: &[f32],
        p_target: &[f32],
        r_samples: &[f32],
        residual_fallback_token: u32,
    ) -> Vec<u32> {
        let k = draft_tokens
            .len()
            .min(p_draft.len())
            .min(p_target.len())
            .min(r_samples.len())
            .min(self.config.lookahead_k as usize);
        let mut accepted = Vec::with_capacity(k + 1);
        for i in 0..k {
            let alpha = Self::acceptance_probability(p_target[i], p_draft[i]);
            if r_samples[i] <= alpha {
                accepted.push(draft_tokens[i]);
            } else {
                accepted.push(residual_fallback_token);
                return accepted;
            }
        }
        accepted
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_speculative_acceptance_and_fallback() {
        let streamer = SpeculativeStreamer::new(SpeculativeStreamerConfig::default());
        let draft = vec![101, 102, 103, 104, 105];
        let p_draft = vec![0.8, 0.7, 0.9, 0.6, 0.8];
        let p_target = vec![0.85, 0.75, 0.2, 0.6, 0.8];
        let r = vec![0.5, 0.5, 0.5, 0.5, 0.5];
        let out = streamer.verify_speculative_step(&draft, &p_draft, &p_target, &r, 999);
        assert_eq!(out, vec![101, 102, 999]);
    }
}
