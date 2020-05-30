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

async function setManualAI() {
  if (highlighted) {
    const response = await fetch(`/api/rooms/testroom/entities/${highlighted}`);
    const entity = await response.json();
    await fetch(`/api/rooms/testroom/entities/${highlighted}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...entity, ai: "manual" }),
    });
    update();
  }
}

async function takeManualAction(action) {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/testroom/agents/${highlighted}/setmove`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(action),
      }
    );
    if (response.ok) {
      await step();
    }
  }
}

init();
document
  .querySelector("#restart-button")
  .addEventListener("click", function () {
    init();
    this.blur();
  });
document
  .querySelector("#manual-ai-button")
  .addEventListener("click", function () {
    setManualAI();
    this.blur();
  });
document.addEventListener("keydown", ({ key }) => {
  switch (key) {
    case " ":
      step();
      break;
    case "ArrowLeft":
      takeManualAction("move_left");
      break;
    case "ArrowRight":
      takeManualAction("move_right");
      break;
    case "ArrowDown":
      takeManualAction("move_down");
      break;
    case "ArrowUp":
      takeManualAction("move_up");
      break;
    default:
      break;
  }
});
