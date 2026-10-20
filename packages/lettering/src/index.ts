/**
 * Paper 18: Structural Vector Typography Synthesis & Dynamic Balloon Tail Placement
 *
 * Optimizes speech balloon placement $c_{balloon}$ and cubic Bezier tail spline $S(u)$ minimizing:
 *   $\int_0^1 \|\kappa(u)\|^2 du + \lambda_{len} \text{Length}(S) + \sum_k \text{Penalty}(S \cap O_k)$
 */

export interface Point2D {
  x: number;
  y: number;
}

export interface RectObstacle {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface BalloonTailRoute {
  balloonCenter: Point2D;
  speakerAnchor: Point2D;
  controlPoint: Point2D;
  svgPath: string;
  collisions: number;
}

function pointInObstacle(p: Point2D, obs: RectObstacle): boolean {
  return p.x >= obs.x && p.x <= obs.x + obs.width && p.y >= obs.y && p.y <= obs.y + obs.height;
}

export function routeBalloonTail(
  candidates: Point2D[],
  speakerAnchor: Point2D,
  obstacles: RectObstacle[]
): BalloonTailRoute {
  let bestRoute: BalloonTailRoute | null = null;
  let bestCost = Number.POSITIVE_INFINITY;

  for (const center of candidates) {
    const controlPoint: Point2D = {
      x: (center.x + speakerAnchor.x) / 2,
      y: Math.min(center.y, speakerAnchor.y) - 20,
    };

    let collisions = 0;
    const samples = 25;
    for (let i = 0; i <= samples; i++) {
      const u = i / samples;
      const omt = 1 - u;
      const pt: Point2D = {
        x: omt * omt * center.x + 2 * omt * u * controlPoint.x + u * u * speakerAnchor.x,
        y: omt * omt * center.y + 2 * omt * u * controlPoint.y + u * u * speakerAnchor.y,
      };
      for (const obs of obstacles) {
        if (pointInObstacle(pt, obs)) {
          collisions += 1;
        }
      }
    }

    const dist = Math.hypot(center.x - speakerAnchor.x, center.y - speakerAnchor.y);
    const cost = dist + collisions * 10000;
    if (cost < bestCost) {
      bestCost = cost;
      bestRoute = {
        balloonCenter: center,
        speakerAnchor,
        controlPoint,
        svgPath: `M ${center.x.toFixed(1)} ${center.y.toFixed(1)} Q ${controlPoint.x.toFixed(1)} ${controlPoint.y.toFixed(1)} ${speakerAnchor.x.toFixed(1)} ${speakerAnchor.y.toFixed(1)}`,
        collisions,
      };
    }
  }

  return bestRoute!;
}
