//! Paper 36: Nash Equilibrium in Autonomous Agent Labor Markets
//!
//! Double auction with buyer bids $b_i$ and seller asks $a_j$.
//! Market clearing price maximizing social welfare:
//! $P^* = \frac{b_{(M)} + a_{(M)}}{2}$

#[derive(Debug, Clone)]
pub struct ClearingResult {
    pub clearing_price: f64,
    pub matched_quantity: usize,
    pub social_welfare: f64,
}

pub struct DoubleAuctionMarket {
    pub buyer_bids: Vec<f64>,
    pub seller_asks: Vec<f64>,
}

impl DoubleAuctionMarket {
    pub fn new(buyer_bids: Vec<f64>, seller_asks: Vec<f64>) -> Self {
        Self {
            buyer_bids,
            seller_asks,
        }
    }

    pub fn clear_market(&self) -> Option<ClearingResult> {
        let mut bids = self.buyer_bids.clone();
        let mut asks = self.seller_asks.clone();
        // Sort bids descending, asks ascending
        bids.sort_by(|a, b| b.partial_cmp(a).unwrap());
        asks.sort_by(|a, b| a.partial_cmp(b).unwrap());

        let limit = bids.len().min(asks.len());
        let mut m = 0;
        let mut welfare = 0.0;
        for i in 0..limit {
            if bids[i] >= asks[i] {
                m = i + 1;
                welfare += bids[i] - asks[i];
            } else {
                break;
            }
        }

        if m == 0 {
            return None;
        }
        let clearing_price = 0.5 * (bids[m - 1] + asks[m - 1]);
        Some(ClearingResult {
            clearing_price,
            matched_quantity: m,
            social_welfare: welfare,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_double_auction_clearing_price() {
        let market = DoubleAuctionMarket::new(
            vec![10.0, 9.0, 8.0, 6.0, 4.0],
            vec![3.0, 5.0, 7.0, 8.5, 9.5],
        );
        let res = market.clear_market().unwrap();
        assert_eq!(res.matched_quantity, 3);
        assert!((res.clearing_price - 7.5).abs() < 1e-6);
    }
}
