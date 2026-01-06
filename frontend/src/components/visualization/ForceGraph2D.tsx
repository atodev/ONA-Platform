import React, { useRef, useCallback } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { GraphData } from "../../types/graph";

interface ForceGraph2DProps {
  data: GraphData;
  onNodeClick?: (node: any) => void;
  onNodeHover?: (node: any) => void;
  height?: number;
  width?: number;
}

export const ForceGraph2DComponent: React.FC<ForceGraph2DProps> = ({
  data,
  onNodeClick,
  onNodeHover,
  height = 600,
  width = 800,
}) => {
  const forceRef = useRef<any>();

  const handleNodeClick = useCallback(
    (node: any) => {
      if (onNodeClick) {
        onNodeClick(node);
      }

      // Center camera on node
      if (forceRef.current) {
        forceRef.current.centerAt(node.x, node.y, 1000);
        forceRef.current.zoom(2, 1000);
      }
    },
    [onNodeClick]
  );

  const nodeCanvasObject = useCallback(
    (node: any, ctx: CanvasRenderingContext2D) => {
      // Custom node rendering
      const size = node.size || 5;
      const color = node.color || "#1976d2";

      // Draw node
      ctx.beginPath();
      ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
      ctx.fillStyle = color;
      ctx.fill();

      // Draw label
      if (node.label) {
        ctx.font = "10px Arial";
        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";
        ctx.fillText(node.label, node.x, node.y + size + 12);
      }
    },
    []
  );

  return (
    <ForceGraph2D
      ref={forceRef}
      graphData={data}
      height={height}
      width={width}
      nodeLabel="id"
      nodeColor={(node: any) => node.color || "#1976d2"}
      nodeRelSize={5}
      linkColor={() => "rgba(255,255,255,0.2)"}
      linkWidth={(link: any) => Math.sqrt(link.weight || 1)}
      onNodeClick={handleNodeClick}
      onNodeHover={onNodeHover}
      nodeCanvasObject={nodeCanvasObject}
      cooldownTicks={100}
      onEngineStop={() => forceRef.current?.zoomToFit(400)}
    />
  );
};
