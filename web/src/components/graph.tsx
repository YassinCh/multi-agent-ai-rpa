import { initialNodes, initialEdges } from "./initialElements";
import ELK from "elkjs/lib/elk.bundled.js";
import React, { useCallback, useLayoutEffect } from "react";
import {
  Background,
  Controls,
  ReactFlow,
  addEdge,
  Panel,
  useNodesState,
  useEdgesState,
  useReactFlow,
  type Node,
  type Edge,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

import StyledNode from './StyledNode';
import StyledEdge from './StyledEdge';
import { RiRobot2Line } from "react-icons/ri";

const elk = new ELK();

const elkOptions = {
  "elk.algorithm": "layered",
  "elk.layered.spacing.nodeNodeBetweenLayers": "130",
  "elk.spacing.nodeNode": "40",
};

const getLayoutedElements = (
  nodes: Node[],
  edges: Edge[],
  options: { [key: string]: any } = {}
) => {
  const isHorizontal = options?.["elk.direction"] === "RIGHT";
  const graph = {
    id: "root",
    layoutOptions: options,
    children: nodes.map((node: Node) => ({
      ...node,
      // Adjust the target and source handle positions based on the layout
      // direction.
      targetPosition: isHorizontal ? "left" : "left",
      sourcePosition: isHorizontal ? "right" : "right",

      // Hardcode a width and height for elk to use when layouting.
      width: 150,
      height: 50,
    })),
    edges: edges.map((edge) => ({
      ...edge,
      sources: [edge.source],
      targets: [edge.target],
    })),
  };

  return elk
    .layout(graph)
    .then((layoutedGraph) => ({
      nodes: layoutedGraph.children!.map((node) => ({
        ...node,
        // React Flow expects a position property on the node instead of `x`
        // and `y` fields.
        position: { x: node.x, y: node.y },
      })),

      edges: layoutedGraph.edges,
    }))
    .catch(console.error);
};

export default function Graph() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);
  const { fitView } = useReactFlow();

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onLayout = useCallback(
    ({
      direction,
      useInitialNodes = false,
    }: {
      direction: string;
      useInitialNodes?: boolean;
    }) => {
      const opts = { "elk.direction": direction, ...elkOptions };
      const ns = useInitialNodes ? initialNodes : nodes;
      const es = useInitialNodes ? initialEdges : edges;

      getLayoutedElements(ns, es, opts).then(
        ({ nodes: layoutedNodes, edges: layoutedEdges }) => {
          setNodes(layoutedNodes);
          setEdges(layoutedEdges);

          window.requestAnimationFrame(() => fitView());
        }
      );
    },
    [nodes, edges]
  );

  // Calculate the initial layout on mount.
  useLayoutEffect(() => {
    onLayout({ direction: "RIGHT", useInitialNodes: true });
  }, []);

  const nodeTypes = {
    styled: StyledNode,
  };
  
  const edgeTypes = {
    styled: StyledEdge,
  };

  const defaultEdgeOptions = {
    type: 'styled',
    markerEnd: 'edge-triangle',
  };

  return (
    <>
      <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      fitView
      nodeTypes={nodeTypes}
      edgeTypes={edgeTypes}
      defaultEdgeOptions={defaultEdgeOptions}
      proOptions={{ hideAttribution: true }}
      colorMode="dark"    
      >
      <Controls showInteractive={false} />
      <svg>
        <defs>
          <linearGradient id="edge-gradient">
            <stop offset="0%" stopColor="#7B1E28" />
            <stop offset="100%" stopColor="#B3202B" />
          </linearGradient>

          <marker
            id="edge-triangle"
            viewBox="-10 -10 20 20"
            refX="-8"
            refY="0"
            markerWidth="12"
            markerHeight="12"
            orient="auto-start-reverse"
          >
            <path
              d="M 0 0 L -8 -8 L -8 8 Z"
              fill="url(#edge-gradient)"
              stroke="none"
            />
          </marker>
        </defs>
      </svg>
      <button className="layout-button" onClick={() => onLayout({ direction: "RIGHT" })}>
        Reorganize Layout
      </button>
      <Background />
    </ReactFlow>
    </>
  );
}
