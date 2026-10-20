/**
 * Paper 29: Proof-of-Human-In-The-Loop: Byzantine Fault Tolerant Curatorial Consensus
 *
 * Staked vote $v_i \in \{0, 1\}$ with stake $w_i$.
 * Consensus outcome: $V^* = \mathbb{I}(\sum_{v_i=1} w_i > \sum_{v_i=0} w_i)$
 * Reward/slashing:
 *   $+R \cdot (w_i / W_{consensus})$ if $v_i = V^*$, else $-w_i \cdot \rho_{slash}$
 */

export interface CuratorVote {
  curatorId: string;
  approve: boolean;
  stake: number;
}

export interface SettlementEntry {
  curatorId: string;
  deltaStake: number;
  finalStake: number;
  slashed: boolean;
}

export function resolveSchellingRound(
  votes: CuratorVote[],
  rewardPool: number,
  slashRatio: number
): { approved: boolean; settlements: SettlementEntry[] } {
  const stakeApprove = votes.filter((v) => v.approve).reduce((acc, v) => acc + v.stake, 0);
  const stakeReject = votes.filter((v) => !v.approve).reduce((acc, v) => acc + v.stake, 0);
  const approved = stakeApprove > stakeReject;
  const consensusStake = approved ? stakeApprove : stakeReject;

  const settlements = votes.map((v) => {
    if (v.approve === approved && consensusStake > 0) {
      const delta = rewardPool * (v.stake / consensusStake);
      return {
        curatorId: v.curatorId,
        deltaStake: delta,
        finalStake: v.stake + delta,
        slashed: false,
      };
    } else {
      const penalty = -v.stake * slashRatio;
      return {
        curatorId: v.curatorId,
        deltaStake: penalty,
        finalStake: v.stake + penalty,
        slashed: true,
      };
    }
  });

  return { approved, settlements };
}
