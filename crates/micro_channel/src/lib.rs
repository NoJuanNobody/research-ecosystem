//! Paper 28: Agent-to-Agent Micro-Streaming Payment Channels via Layer-2 State Channels
//!
//! Off-chain state channel updates signed by both agents at sequence $k$:
//! $\sigma_k = \text{Sign}_{Alice}(H(k, \text{bal}_A, \text{bal}_B))$,
//! $\tau_k = \text{Sign}_{Bob}(H(k, \text{bal}_A, \text{bal}_B))$

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChannelVoucher {
    pub sequence_k: u64,
    pub balance_a: u64,
    pub balance_b: u64,
    pub sig_alice: u64,
    pub sig_bob: u64,
}

pub struct StateChannel {
    pub total_deposit: u64,
    pub latest_voucher: ChannelVoucher,
    pub alice_key: u64,
    pub bob_key: u64,
}

impl StateChannel {
    pub fn open(deposit_a: u64, deposit_b: u64, alice_key: u64, bob_key: u64) -> Self {
        let mut ch = Self {
            total_deposit: deposit_a + deposit_b,
            latest_voucher: ChannelVoucher {
                sequence_k: 0,
                balance_a: deposit_a,
                balance_b: deposit_b,
                sig_alice: 0,
                sig_bob: 0,
            },
            alice_key,
            bob_key,
        };
        let (sa, sb) = ch.sign_state(0, deposit_a, deposit_b);
        ch.latest_voucher.sig_alice = sa;
        ch.latest_voucher.sig_bob = sb;
        ch
    }

    fn state_digest(k: u64, bal_a: u64, bal_b: u64) -> u64 {
        k.wrapping_mul(0x9E3779B97F4A7C15)
            ^ bal_a.wrapping_mul(0xBF58476D1CE4E5B9)
            ^ bal_b.wrapping_mul(0x94D049BB133111EB)
    }

    pub fn sign_state(&self, k: u64, bal_a: u64, bal_b: u64) -> (u64, u64) {
        let digest = Self::state_digest(k, bal_a, bal_b);
        (digest ^ self.alice_key, digest ^ self.bob_key)
    }

    pub fn stream_micro_payment(&mut self, amount_a_to_b: u64) -> Result<ChannelVoucher, &'static str> {
        if self.latest_voucher.balance_a < amount_a_to_b {
            return Err("insufficient channel balance");
        }
        let next_k = self.latest_voucher.sequence_k + 1;
        let next_a = self.latest_voucher.balance_a - amount_a_to_b;
        let next_b = self.latest_voucher.balance_b + amount_a_to_b;
        let (sig_a, sig_b) = self.sign_state(next_k, next_a, next_b);
        let voucher = ChannelVoucher {
            sequence_k: next_k,
            balance_a: next_a,
            balance_b: next_b,
            sig_alice: sig_a,
            sig_bob: sig_b,
        };
        self.latest_voucher = voucher.clone();
        Ok(voucher)
    }

    pub fn settle(vouchers: &[ChannelVoucher], total_deposit: u64, alice_key: u64, bob_key: u64) -> Option<ChannelVoucher> {
        vouchers
            .iter()
            .filter(|v| {
                if v.balance_a + v.balance_b != total_deposit {
                    return false;
                }
                let d = Self::state_digest(v.sequence_k, v.balance_a, v.balance_b);
                v.sig_alice == (d ^ alice_key) && v.sig_bob == (d ^ bob_key)
            })
            .max_by_key(|v| v.sequence_k)
            .cloned()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_micro_streaming_and_maximal_sequence_settlement() {
        let mut ch = StateChannel::open(10_000, 0, 0xAAAA, 0xBBBB);
        let v1 = ch.stream_micro_payment(250).unwrap();
        let v2 = ch.stream_micro_payment(750).unwrap();
        let settled = StateChannel::settle(&[v1, v2.clone()], 10_000, 0xAAAA, 0xBBBB).unwrap();
        assert_eq!(settled.sequence_k, 2);
        assert_eq!(settled.balance_a, 9_000);
        assert_eq!(settled.balance_b, 1_000);
    }
}
