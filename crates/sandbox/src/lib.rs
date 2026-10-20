//! Paper 10: Fault-Tolerant Speculative Agent Tool Sandboxing with Deterministic Rollbacks
//!
//! Copy-on-write (CoW) sandbox where a speculative tool trajectory $\tau = (a_1, \dots, a_n)$
//! executes in an ephemeral branch and rolls back via inverse delta operations:
//! $\mathcal{S}_{reverted} = \mathcal{S}_{current} \circ \Delta_n^{-1} \circ \dots \circ \Delta_1^{-1}$

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FileDelta {
    pub path: String,
    pub previous_bytes: Option<Vec<u8>>,
    pub next_bytes: Option<Vec<u8>>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SandboxError {
    NoActiveTurn,
    InvariantViolation(String),
}

pub struct TransactionalSandbox {
    pub snapshot_id: String,
    pub committed_fs: BTreeMap<String, Vec<u8>>,
    pub overlay_fs: BTreeMap<String, Vec<u8>>,
    pub write_journal: Vec<FileDelta>,
    pub active_turn: bool,
}

impl TransactionalSandbox {
    pub fn new(initial_fs: BTreeMap<String, Vec<u8>>) -> Self {
        Self {
            snapshot_id: "snap-0".to_string(),
            overlay_fs: initial_fs.clone(),
            committed_fs: initial_fs,
            write_journal: Vec::new(),
            active_turn: false,
        }
    }

    pub fn begin_speculative_turn(&mut self, turn_id: &str) -> Result<String, SandboxError> {
        self.snapshot_id = turn_id.to_string();
        self.overlay_fs = self.committed_fs.clone();
        self.write_journal.clear();
        self.active_turn = true;
        Ok(self.snapshot_id.clone())
    }

    pub fn write_file(&mut self, path: &str, content: Vec<u8>) -> Result<(), SandboxError> {
        if !self.active_turn {
            return Err(SandboxError::NoActiveTurn);
        }
        let prev = self.overlay_fs.insert(path.to_string(), content.clone());
        self.write_journal.push(FileDelta {
            path: path.to_string(),
            previous_bytes: prev,
            next_bytes: Some(content),
        });
        Ok(())
    }

    pub fn delete_file(&mut self, path: &str) -> Result<(), SandboxError> {
        if !self.active_turn {
            return Err(SandboxError::NoActiveTurn);
        }
        let prev = self.overlay_fs.remove(path);
        self.write_journal.push(FileDelta {
            path: path.to_string(),
            previous_bytes: prev,
            next_bytes: None,
        });
        Ok(())
    }

    pub fn commit(&mut self) -> Result<(), SandboxError> {
        if !self.active_turn {
            return Err(SandboxError::NoActiveTurn);
        }
        self.committed_fs = self.overlay_fs.clone();
        self.write_journal.clear();
        self.active_turn = false;
        Ok(())
    }

    pub fn rollback(&mut self) -> Result<(), SandboxError> {
        if !self.active_turn {
            return Err(SandboxError::NoActiveTurn);
        }
        while let Some(delta) = self.write_journal.pop() {
            match delta.previous_bytes {
                Some(bytes) => {
                    self.overlay_fs.insert(delta.path, bytes);
                }
                None => {
                    self.overlay_fs.remove(&delta.path);
                }
            }
        }
        self.active_turn = false;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_transactional_rollback_restores_exact_bytes() {
        let mut init = BTreeMap::new();
        init.insert("/etc/config.json".to_string(), b"{\"safe\":true}".to_vec());
        let mut sb = TransactionalSandbox::new(init.clone());

        sb.begin_speculative_turn("turn-1").unwrap();
        sb.write_file("/etc/config.json", b"CORRUPTED".to_vec()).unwrap();
        sb.write_file("/tmp/malicious.sh", b"rm -rf /".to_vec()).unwrap();
        sb.rollback().unwrap();

        assert_eq!(sb.overlay_fs, init);
        assert_eq!(sb.committed_fs, init);
    }
}
