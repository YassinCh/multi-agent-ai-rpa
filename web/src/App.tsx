import React, { useCallback } from 'react';
import {
  ReactFlow,
  Controls,
  useNodesState,
  useEdgesState,
  addEdge,
  type Node,
  type Edge,
  type OnConnect,
} from '@xyflow/react';
import { FiFile } from 'react-icons/fi';
import { RiRobot2Fill } from "react-icons/ri";

import '@xyflow/react/dist/base.css';

import TurboNode, { type TurboNodeData } from './TurboNode';

import TurboEdge from './TurboEdge';
import './styles/index.css';

const initialNodes: Node<TurboNodeData>[] = [
  {
    id: '1',
    position: { x: 0, y: 0 },
    data: { icon: <RiRobot2Fill />, title: 'readFile', active: false },
    type: 'turbo',
  },
  {
    id: '2',
    position: { x: 250, y: 0 },
    data: { icon: <RiRobot2Fill />, title: 'bundle', active: false },
    type: 'turbo',
  },
  {
    id: '3',
    position: { x: 0, y: 250 },
    data: { icon: <RiRobot2Fill />, title: 'readFile', active: false },
    type: 'turbo',
  },
  {
    id: '4',
    position: { x: 250, y: 250 },
    data: { icon: <RiRobot2Fill />, title: 'bundle', active: true },
    type: 'turbo',
  },
  {
    id: '5',
    position: { x: 500, y: 125 },
    data: { icon: <RiRobot2Fill />, title: 'concat', active: false },
    type: 'turbo',
  },
  {
    id: '6',
    position: { x: 750, y: 125 },
    data: { icon: <RiRobot2Fill />, title: 'fullBundle', active: false },
    type: 'turbo',
  },
];

const initialEdges: Edge[] = [
  {
    id: 'e1-2',
    source: '1',
    target: '2',
  },
  {
    id: 'e3-4',
    source: '3',
    target: '4',
  },
  {
    id: 'e2-5',
    source: '2',
    target: '5',
  },
  {
    id: 'e4-5',
    source: '4',
    target: '5'
  },
  {
    id: 'e5-6',
    source: '5',
    target: '6',
    markerStart: 'edge-triangle',
    markerEnd: 'edge-triangle',
  }
];

const nodeTypes = {
  turbo: TurboNode,
};

const edgeTypes = {
  turbo: TurboEdge,
};

const defaultEdgeOptions = {
  type: 'turbo',
  markerEnd: 'edge-triangle',
};

const Flow = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect: OnConnect = useCallback(
    (params) => setEdges((els) => addEdge(params, els)),
    [],
  );

  return (
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
            refX="0"
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
    </ReactFlow>
  );
};

export default Flow;
