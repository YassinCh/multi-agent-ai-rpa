import { initialNodes, initialEdges } from "./initialElements";
import ELK from "elkjs/lib/elk.bundled.js";
import React, { useCallback, useLayoutEffect } from "react";
import {
  Background,
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

const elk = new ELK();

const elkOptions = {
  "elk.algorithm": "layered",
  "elk.layered.spacing.nodeNodeBetweenLayers": "100",
  "elk.spacing.nodeNode": "80",
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
      targetPosition: isHorizontal ? "left" : "top",
      sourcePosition: isHorizontal ? "right" : "bottom",

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
    onLayout({ direction: "DOWN", useInitialNodes: true });
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onConnect={onConnect}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        style={{ backgroundColor: "#F7F9FB" }}
      >
        <Panel position="top-right">
          <button onClick={() => onLayout({ direction: "DOWN" })}>
            vertical layout
          </button>

          <button onClick={() => onLayout({ direction: "RIGHT" })}>
            horizontal layout
          </button>
        </Panel>
        <Background />
      </ReactFlow>
    </div>
  );
}
