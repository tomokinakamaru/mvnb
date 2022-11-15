import * as state from "./state";
import { CreateCell, DeleteCell, Notebook, Stdout } from "./types";
import * as websocket from "./websocket";
import { v4 as uuid } from "uuid";

export const saveNotebook = () => {
  websocket.send({ _type: "SaveNotebook" });
};

export const createCell = (parent: string | null) => {
  websocket.send({ _type: "CreateCell", cell: uuid(), parent: parent });
};

export const deleteCell = (id: string) => {
  websocket.send({ _type: "DeleteCell", cell: id });
};

export const updateCell = (id: string, source: string) => {
  websocket.send({ _type: "UpdateCell", cell: id, source: source });
};

export const runCell = (id: string) => {
  websocket.send({ _type: "RunCell", cell: id });
};

const onMessage = (type: string, data: any) => {
  if (type === "Notebook") {
    for (const cell of (data as Notebook).cells) {
      createNode(cell.id, cell.parent);
      createEdge(cell.parent, cell.id);
    }
  } else if (type === "DidCreateCell") {
    const request = data.request as CreateCell;
    createNode(request.cell, request.parent);
    createEdge(request.parent, request.cell);
  } else if (type === "DidDeleteCell") {
    const request = data.request as DeleteCell;
    deleteNode(request.cell);
    deleteEdge(request.cell);
  } else if (type === "Stdout") {
    console.log(data);
    const stdout = data as Stdout;
    state.setOutputs(stdout.cell, (os) => [
      ...os,
      { type: "text", data: stdout.text },
    ]);
  }
};

const createNode = (id: string, parent: string | null) => {
  state.setNodes((nodes) => {
    const type = "cell";
    const data = { id, parent, source: "", outputs: [] };
    const position = { x: 0, y: 0 };
    return [...nodes, { id, data, type, position }];
  });
};

const deleteNode = (id: string) => {
  state.setNodes((nodes) => {
    return nodes.filter((n) => n.id != id);
  });
};

const deleteEdge = (id: string) => {
  state.setEdges((edges) => {
    return edges.filter((e) => e.source != id && e.target != id);
  });
};

const createEdge = (source: string | null, target: string) => {
  if (source) {
    const id = createEdgeId(source, target);
    state.setEdges((edges) => [...edges, { id, source, target }]);
  }
};

const createEdgeId = (source: string, target: string) => `${source}_${target}`;

websocket.setListener(onMessage);