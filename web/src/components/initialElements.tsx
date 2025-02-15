const position = { x: 0, y: 0 };

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

import { type StyledNodeData } from './StyledNode';
import { RiRobot2Fill } from "react-icons/ri";
import '../styles/flow.css';


export const initialNodes: Node<StyledNodeData>[] = [
  {
    id: "1",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 1', active: false },
    type: 'styled',
  },  
  {
    id: "2",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 2', active: false },
    type: 'styled',
  },
  {
    id: "2a",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 3', active: false },
    type: 'styled',
  },
  {
    id: "2b",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 4', active: false },
    type: 'styled',
  },
  {
    id: "2c",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 5', active: false },
    type: 'styled',
  },
  {
    id: "2d",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 6', active: false },
    type: 'styled',
  },  
  {
    id: "3",
    position,
    data: { icon: <RiRobot2Fill />, title: 'Agent 7', active: false },
    type: 'styled',
  },

];

export const initialEdges:Edge[] = [
  { id: "e12", source: "1", target: "2", type: "smoothstep" },
  { id: "e13", source: "1", target: "3", type: "smoothstep" },
  { id: "e22a", source: "2", target: "2a", type: "smoothstep" },
  { id: "e22b", source: "2", target: "2b", type: "smoothstep" },
  { id: "e22c", source: "2", target: "2c", type: "smoothstep" },
  { id: "e2c2d", source: "2c", target: "2d", type: "smoothstep" }
];
