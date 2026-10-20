//! Paper 02: Stateful Delta-KV Cache Compression Hierarchy for Persistent Local Agents
//!
//! Partitions sequence index $t \in [0, T]$ into:
//! - Attention Sinks $S = [0, S_{sink}]$ (first 4 tokens preserved)
//! - Active Window $W = [T - W_{active}, T]$ (FP8 quantized)
//! - Evicted Delta Region $E$: $k_t = c_j + r_t, \|r_t\|_0 \le \epsilon$

#[derive(Debug, Clone)]
pub struct DeltaEntry {
    pub centroid_idx: usize,
    pub sparse_residuals: Vec<(usize, f32)>,
}

#[derive(Debug, Clone)]
pub struct HierarchicalKVCache {
    pub sink_keys: Vec<Vec<f32>>,
    pub active_window_keys: Vec<Vec<i8>>, // FP8/INT8 quantized active window
    pub centroid_table: Vec<Vec<f32>>,
    pub evicted_deltas: Vec<DeltaEntry>,
    pub sink_size: usize,
    pub window_size: usize,
    pub sparsity_budget: usize,
}

impl HierarchicalKVCache {
    pub fn new(sink_size: usize, window_size: usize, sparsity_budget: usize, centroids: Vec<Vec<f32>>) -> Self {
        Self {
            sink_keys: Vec::new(),
            active_window_keys: Vec::new(),
            centroid_table: centroids,
            evicted_deltas: Vec::new(),
            sink_size,
            window_size,
            sparsity_budget,
        }
    }

    pub fn append_key(&mut self, key: Vec<f32>) {
        if self.sink_keys.len() < self.sink_size {
            self.sink_keys.push(key);
            return;
        }
        let quantized: Vec<i8> = key
            .iter()
            .map(|&v| (v.clamp(-1.0, 1.0) * 127.0).round() as i8)
            .collect();
        self.active_window_keys.push(quantized);

        if self.active_window_keys.len() > self.window_size {
            let evicted_q = self.active_window_keys.remove(0);
            let evicted_f32: Vec<f32> = evicted_q.iter().map(|&q| (q as f32) / 127.0).collect();
            let delta = self.compress_to_delta(&evicted_f32);
            self.evicted_deltas.push(delta);
        }
    }

    fn compress_to_delta(&self, key: &[f32]) -> DeltaEntry {
        let mut best_idx = 0;
        let mut best_dist = f32::MAX;
        for (idx, c) in self.centroid_table.iter().enumerate() {
            let dist: f32 = key.iter().zip(c.iter()).map(|(a, b)| (a - b).powi(2)).sum();
            if dist < best_dist {
                best_dist = dist;
                best_idx = idx;
            }
        }
        let centroid = &self.centroid_table[best_idx];
        let mut diffs: Vec<(usize, f32)> = key
            .iter()
            .zip(centroid.iter())
            .enumerate()
            .map(|(i, (&k, &c))| (i, k - c))
            .collect();
        diffs.sort_by(|a, b| b.1.abs().partial_cmp(&a.1.abs()).unwrap());
        diffs.truncate(self.sparsity_budget);
        DeltaEntry {
            centroid_idx: best_idx,
            sparse_residuals: diffs,
        }
    }

    pub fn reconstruct_evicted(&self, idx: usize) -> Vec<f32> {
        let entry = &self.evicted_deltas[idx];
        let mut out = self.centroid_table[entry.centroid_idx].clone();
        for &(dim, val) in &entry.sparse_residuals {
            out[dim] += val;
        }
        out
    }

    pub fn cosine_similarity(a: &[f32], b: &[f32]) -> f32 {
        let dot: f32 = a.iter().zip(b.iter()).map(|(x, y)| x * y).sum();
        let na: f32 = a.iter().map(|x| x * x).sum::<f32>().sqrt();
        let nb: f32 = b.iter().map(|x| x * x).sum::<f32>().sqrt();
        if na == 0.0 || nb == 0.0 {
            0.0
        } else {
            dot / (na * nb)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kv_hierarchy_and_reconstruction() {
        let centroids = vec![vec![0.5, 0.5, 0.5, 0.5], vec![-0.5, -0.5, -0.5, -0.5]];
        let mut cache = HierarchicalKVCache::new(4, 2, 3, centroids);
        for _ in 0..4 {
            cache.append_key(vec![0.1, 0.1, 0.1, 0.1]);
        }
        let target_key = vec![0.52, 0.48, 0.55, 0.50];
        cache.append_key(target_key.clone());
        cache.append_key(vec![0.4, 0.4, 0.4, 0.4]);
        cache.append_key(vec![0.3, 0.3, 0.3, 0.3]);

        assert_eq!(cache.sink_keys.len(), 4);
        assert_eq!(cache.active_window_keys.len(), 2);
        assert_eq!(cache.evicted_deltas.len(), 1);

        let recon = cache.reconstruct_evicted(0);
        assert!(HierarchicalKVCache::cosine_similarity(&target_key, &recon) > 0.99);
    }
}
