/**
 * Paper 13: Deterministic Time-Indexed Frame Synthesis in Headless Render Graphs
 *
 * Models canvas state as a pure function of continuous time $t$:
 *   $\mathbf{C}(t) = \bigoplus_{i=1}^N \mathcal{R}_i(\theta_i(t), \mathcal{A}_i)$
 * Loop boundary condition for period $T$:
 *   $\|\mathbf{C}(0) - \mathbf{C}(T)\|_\infty = 0$ and $\left.\frac{d\mathbf{C}}{dt}\right|_{t=0} = \left.\frac{d\mathbf{C}}{dt}\right|_{t=T}$
 */

import { createHash } from "crypto";

export interface LayerSpec {
  id: string;
  amplitude: number;
  frequencyHz: number;
  phaseRad: number;
  baseValue: number;
}

export interface TimeIndexedScene {
  durationSeconds: number;
  fps: number;
  layers: LayerSpec[];
}

export function evaluateCanvasState(scene: TimeIndexedScene, t: number): number[] {
  const period = scene.durationSeconds;
  const omega = (2 * Math.PI) / period;
  return scene.layers.map((layer) => {
    const harmonic = Math.round(layer.frequencyHz * period) || 1;
    return layer.baseValue + layer.amplitude * Math.sin(harmonic * omega * t + layer.phaseRad);
  });
}

export function frameHashSha256(scene: TimeIndexedScene, frameIndex: number): string {
  const t = frameIndex / scene.fps;
  const state = evaluateCanvasState(scene, t).map((v) => v.toFixed(8));
  return createHash("sha256").update(JSON.stringify({ frameIndex, state })).digest("hex");
}

export function verifyLoopSeam(scene: TimeIndexedScene): { maxSeamError: number; seamless: boolean } {
  const c0 = evaluateCanvasState(scene, 0);
  const cT = evaluateCanvasState(scene, scene.durationSeconds);
  const maxSeamError = c0.reduce((acc, v, idx) => Math.max(acc, Math.abs(v - cT[idx])), 0);
  return { maxSeamError, seamless: maxSeamError < 1e-9 };
}
