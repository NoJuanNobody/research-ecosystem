//! Paper 05: Neuro-Symbolic Micro-Guardrail Verification on Microcontrollers
//!
//! Freestanding `#![no_std]` Deterministic Finite Automaton (DFA) AST validator:
//! $q_{t+1} = \delta(q_t, c_t)$; aborts immediately at $q_{trap}$ in $<200\mu\text{s}$ with zero heap allocation.

#![no_std]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GuardResult {
    GuardPass,
    GuardTrap,
    GuardBufferOverflow,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DfaState {
    Start,
    InObject,
    InString,
    EscapeNext,
    Complete,
    Trap,
}

pub struct ToolCallContext {
    pub state: DfaState,
    pub depth: usize,
    pub bytes_processed: usize,
    pub max_bytes: usize,
}

impl ToolCallContext {
    pub const fn new(max_bytes: usize) -> Self {
        Self {
            state: DfaState::Start,
            depth: 0,
            bytes_processed: 0,
            max_bytes,
        }
    }
}

pub fn verify_tool_call_token(token: &[u8], ctx: &mut ToolCallContext) -> GuardResult {
    // Reject shell injection sequences immediately (`;`, `|`, `` ` ``, `$`)
    for &b in token {
        ctx.bytes_processed += 1;
        if ctx.bytes_processed > ctx.max_bytes {
            ctx.state = DfaState::Trap;
            return GuardResult::GuardBufferOverflow;
        }
        if b == b';' || b == b'|' || b == b'`' || b == b'$' {
            ctx.state = DfaState::Trap;
            return GuardResult::GuardTrap;
        }

        match ctx.state {
            DfaState::Start => match b {
                b' ' | b'\t' | b'\n' | b'\r' => {}
                b'{' => {
                    ctx.depth = 1;
                    ctx.state = DfaState::InObject;
                }
                _ => {
                    ctx.state = DfaState::Trap;
                    return GuardResult::GuardTrap;
                }
            },
            DfaState::InObject => match b {
                b'"' => ctx.state = DfaState::InString,
                b'{' => ctx.depth += 1,
                b'}' => {
                    ctx.depth -= 1;
                    if ctx.depth == 0 {
                        ctx.state = DfaState::Complete;
                    }
                }
                _ => {}
            },
            DfaState::InString => match b {
                b'\\' => ctx.state = DfaState::EscapeNext,
                b'"' => ctx.state = DfaState::InObject,
                _ => {}
            },
            DfaState::EscapeNext => {
                ctx.state = DfaState::InString;
            }
            DfaState::Complete => match b {
                b' ' | b'\t' | b'\n' | b'\r' => {}
                _ => {
                    ctx.state = DfaState::Trap;
                    return GuardResult::GuardTrap;
                }
            },
            DfaState::Trap => return GuardResult::GuardTrap,
        }
    }
    GuardResult::GuardPass
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dfa_accepts_safe_json_and_traps_injection() {
        let mut ctx = ToolCallContext::new(256);
        let res = verify_tool_call_token(b"{\"tool\":\"set_servo\",\"angle\":45}", &mut ctx);
        assert_eq!(res, GuardResult::GuardPass);
        assert_eq!(ctx.state, DfaState::Complete);

        let mut bad_ctx = ToolCallContext::new(256);
        let bad_res = verify_tool_call_token(b"{\"cmd\":\"run; rm -rf /\"}", &mut bad_ctx);
        assert_eq!(bad_res, GuardResult::GuardTrap);
    }
}
