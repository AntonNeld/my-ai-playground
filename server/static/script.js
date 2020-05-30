import { Room } from "./room.js";

const testRoom = [
  { x: 0, y: 0, type: "player", ai: "pathfinder" },
  { x: -1, y: 1, type: "block" },
  { x: 0, y: 1, type: "block" },
  { x: 1, y: 1, type: "block" },
  { x: 1, y: 0, type: "coin" },
  { x: -1, y: 0, type: "coin" },
];

let room;
let highlighted;

async function init() {
  await fetch("/api/rooms/testroom", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(testRoom),
  });
  room = new Room(document.querySelector(".room-area"));
  highlighted = null;
  room.addEventListener("highlighted", ({ detail: { id } }) => {
    highlighted = id;
    update();
  });

  await update();
}

async function update() {
  const [roomData, entityData] = await Promise.all([
    getRoomData(),
    getEntityData(),
  ]);
  room.setData(roomData);
  document.querySelector("#details-area").innerHTML = entityData
    ? JSON.stringify(entityData, null, 2)
    : "";
}

async function getRoomData() {
  const response = await fetch("/api/rooms/testroom");
  const data = await response.json();
  return data;
}

async function getEntityData() {
  if (highlighted) {
    const response = await fetch(`/api/rooms/testroom/entities/${highlighted}`);
    if (!response.ok) {
      return null;
    }
    const entity = await response.json();
    return entity;
  } else {
    return null;
  }
}

async function step() {
  await fetch("/api/rooms/testroom/step", { method: "POST" });
  update();
}

init();
document
  .querySelector("#restart-button")
  .addEventListener("click", () => init());
document.querySelector("#step-button").addEventListener("click", () => step());
