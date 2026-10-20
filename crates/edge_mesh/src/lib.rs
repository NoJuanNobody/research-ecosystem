//! Paper 04: Edge-to-Edge Gossip Consensus in Ephemeral Agent Meshes
//!
//! State-based Observed-Remove Set (ORSet) CRDT semantics:
//! $S_{merged} = (S_1 \cup S_2) \setminus \{(e, t) \mid (e, t) \in \text{Tombs}_1 \cup \text{Tombs}_2\}$

use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SyncDelta {
    pub added_count: usize,
    pub removed_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MeshError {
    MalformedDigest,
}

pub trait GossipNode {
    fn broadcast_digest(&self) -> ORSetState;
    fn merge_remote_digest(&mut self, remote_digest: &ORSetState) -> Result<SyncDelta, MeshError>;
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct ORSetState {
    pub elements: BTreeSet<(String, String)>, // (element, unique_tag)
    pub tombstones: BTreeSet<(String, String)>,
    pub vector_clock: BTreeMap<String, u64>,
}

pub struct EphemeralMeshNode {
    pub node_id: String,
    pub state: ORSetState,
}

impl EphemeralMeshNode {
    pub fn new(node_id: &str) -> Self {
        Self {
            node_id: node_id.to_string(),
            state: ORSetState::default(),
        }
    }

    pub fn add(&mut self, element: &str) {
        let counter = self.state.vector_clock.entry(self.node_id.clone()).or_insert(0);
        *counter += 1;
        let tag = format!("{}:{}", self.node_id, *counter);
        let pair = (element.to_string(), tag);
        if !self.state.tombstones.contains(&pair) {
            self.state.elements.insert(pair);
        }
    }

    pub fn remove(&mut self, element: &str) {
        let matching: Vec<(String, String)> = self
            .state
            .elements
            .iter()
            .filter(|(e, _)| e == element)
            .cloned()
            .collect();
        for pair in matching {
            self.state.elements.remove(&pair);
            self.state.tombstones.insert(pair);
        }
    }

    pub fn active_values(&self) -> BTreeSet<String> {
        self.state
            .elements
            .iter()
            .filter(|pair| !self.state.tombstones.contains(pair))
            .map(|(e, _)| e.clone())
            .collect()
    }
}

impl GossipNode for EphemeralMeshNode {
    fn broadcast_digest(&self) -> ORSetState {
        self.state.clone()
    }

    fn merge_remote_digest(&mut self, remote: &ORSetState) -> Result<SyncDelta, MeshError> {
        let prev_elements = self.state.elements.len();
        let prev_tombs = self.state.tombstones.len();

        for t in &remote.tombstones {
            self.state.tombstones.insert(t.clone());
        }
        for e in &remote.elements {
            if !self.state.tombstones.contains(e) {
                self.state.elements.insert(e.clone());
            }
        }
        self.state
            .elements
            .retain(|pair| !self.state.tombstones.contains(pair));

        for (peer, &clock) in &remote.vector_clock {
            let entry = self.state.vector_clock.entry(peer.clone()).or_insert(0);
            if clock > *entry {
                *entry = clock;
            }
        }

        Ok(SyncDelta {
            added_count: self.state.elements.len().saturating_sub(prev_elements),
            removed_count: self.state.tombstones.len().saturating_sub(prev_tombs),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_orset_gossip_convergence() {
        let mut node_a = EphemeralMeshNode::new("nodeA");
        let mut node_b = EphemeralMeshNode::new("nodeB");

        node_a.add("task_1");
        node_a.add("task_2");
        node_b.add("task_3");

        let digest_a = node_a.broadcast_digest();
        node_b.merge_remote_digest(&digest_a).unwrap();
        node_b.remove("task_1");

        let digest_b = node_b.broadcast_digest();
        node_a.merge_remote_digest(&digest_b).unwrap();

        assert_eq!(node_a.active_values(), node_b.active_values());
        assert!(!node_a.active_values().contains("task_1"));
        assert!(node_a.active_values().contains("task_2"));
        assert!(node_a.active_values().contains("task_3"));
    }
}
