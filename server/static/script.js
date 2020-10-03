import { Room } from "./room.js";

const roomId = "testroom";

let room;
let highlighted;
let currentChallenge = "maze";
let currentVariant = "standard";
let autoStepTimer = null;

async function getChallenges() {
  const response = await fetch("/api/challenges");
  const challenges = await response.json();
  const select = document.querySelector("#challenge-dropdown");
  while (select.lastChild) {
    select.lastChild.remove();
  }
  challenges.forEach((challenge) => {
    const option = document.createElement("option");
    option.textContent = challenge;
    option.value = challenge;
    select.appendChild(option);
  });
  select.value = currentChallenge;
}

async function getVariants(challenge) {
  const response = await fetch(`/api/challenges/${challenge}/variants`);
  const variants = await response.json();
  const select = document.querySelector("#variant-dropdown");
  if (variants.length == 0) {
    currentVariant = null;
    select.classList.add("hidden");
  } else {
    currentVariant = variants[0];
    select.classList.remove("hidden");
  }
  while (select.lastChild) {
    select.lastChild.remove();
  }
  variants.forEach((variant) => {
    const option = document.createElement("option");
    option.textContent = variant;
    option.value = variant;
    select.appendChild(option);
  });
}

async function initRoom(challenge, variant) {
  clearInterval(autoStepTimer);
  autoStepTimer = null;
  await fetch(
    `/api/rooms/${roomId}?from_challenge=${challenge}${
      variant !== null ? `&variant=${variant}` : ""
    }`,
    {
      method: "PUT",
    }
  );
  room = new Room(document.querySelector(".room-area"));
  highlighted = null;
  room.addEventListener("highlighted", ({ detail: { id } }) => {
    highlighted = id;
    update();
  });

  await update();
}

async function update() {
  const [roomData, entityData, scoreData] = await Promise.all([
    getRoomData(),
    getEntityData(),
    getScoreData(),
  ]);
  room.setData(
    Object.entries(roomData.entities).map(([id, entity]) => ({ id, ...entity }))
  );
  // Use timeout so the browser doesn't scroll to the new data when
  // this is triggered by the user directly
  setTimeout(() => {
    document.querySelector("#details-area").innerHTML = entityData
      ? JSON.stringify(entityData, null, 2)
      : "";
    document.querySelector("#steps").innerHTML = `Steps: ${roomData.steps}`;
    document.querySelector("#score").innerHTML = `Score: ${
      scoreData !== null ? scoreData : "-"
    }`;
  }, 0);
}

async function getRoomData() {
  const response = await fetch(`/api/rooms/${roomId}`);
  const data = await response.json();
  return data;
}

async function getEntityData() {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}`
    );
    if (!response.ok) {
      return null;
    }
    const entity = await response.json();
    return entity;
  } else {
    return null;
  }
}

async function getScoreData() {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}/score`
    );
    if (!response.ok) {
      return null;
    }
    const score = await response.json();
    return score;
  } else {
    return null;
  }
}

async function step() {
  await fetch(`/api/rooms/${roomId}/step`, { method: "POST" });
  update();
}

async function takeManualAction(action) {
  if (highlighted) {
    const response = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}`
    );
    const { ai: oldAi, ...rest } = await response.json();
    await fetch(`/api/rooms/${roomId}/entities/${highlighted}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ai: { kind: "singular", action }, ...rest }),
    });
    await fetch(`/api/rooms/${roomId}/step`, { method: "POST" });
    const newResponse = await fetch(
      `/api/rooms/${roomId}/entities/${highlighted}`
    );
    const entity = await newResponse.json();
    await fetch(`/api/rooms/${roomId}/entities/${highlighted}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...entity, ai: oldAi }),
    });
    update();
  }
}

function toggleAutoStep() {
  if (autoStepTimer) {
    clearInterval(autoStepTimer);
    autoStepTimer = null;
  } else {
    autoStepTimer = setInterval(step, 400);
  }
}

async function evaluateChallenge(challenge, duration) {
  document.querySelector("#details-area").innerHTML = "...";
  const response = await fetch(`/api/evaluate`, {
    method: "POST",
    body: JSON.stringify({
      challenge,
      duration,
      profileTime: true,
      profileMemory: true,
    }),
  });
  const result = await response.json();
  document.querySelector("#details-area").innerHTML = JSON.stringify(
    result,
    null,
    2
  );
}

getChallenges();
getVariants(currentChallenge);
initRoom(currentChallenge, currentVariant);
document
  .querySelector("#restart-button")
  .addEventListener("click", function () {
    initRoom(currentChallenge, currentVariant);
    this.blur();
  });
document
  .querySelector("#challenge-dropdown")
  .addEventListener("change", async function (event) {
    const challenge = event.target.value;
    currentChallenge = challenge;
    await getVariants(challenge);
    initRoom(currentChallenge, currentVariant);
    this.blur();
  });
document
  .querySelector("#variant-dropdown")
  .addEventListener("change", async function (event) {
    const variant = event.target.value;
    currentVariant = variant;
    initRoom(currentChallenge, currentVariant);
    this.blur();
  });
document
  .querySelector("#evaluate-button")
  .addEventListener("click", function (event) {
    const challenge = document.querySelector("#challenge-dropdown").value;
    const duration = document.querySelector("#duration-input").value;
    evaluateChallenge(challenge, duration);
    this.blur();
  });
document.addEventListener("keydown", (event) => {
  if (event.target !== document.body) {
    return;
  }
  event.preventDefault();
  switch (event.key) {
    case " ":
      step();
      break;
    case "ArrowLeft":
      takeManualAction({ actionType: "move", direction: "left" });
      break;
    case "ArrowRight":
      takeManualAction({ actionType: "move", direction: "right" });
      break;
    case "ArrowDown":
      takeManualAction({ actionType: "move", direction: "down" });
      break;
    case "ArrowUp":
      takeManualAction({ actionType: "move", direction: "up" });
      break;
    case "Control":
      takeManualAction({ actionType: "pick_up" });
      break;
    case "1":
      takeManualAction({ actionType: "drop", index: 0 });
      break;
    case "2":
      takeManualAction({ actionType: "drop", index: 1 });
      break;
    case "j":
      takeManualAction({ actionType: "attack", direction: "left" });
      break;
    case "l":
      takeManualAction({ actionType: "attack", direction: "right" });
      break;
    case "k":
      takeManualAction({ actionType: "attack", direction: "down" });
      break;
    case "i":
      takeManualAction({ actionType: "attack", direction: "up" });
      break;
    case "a":
      toggleAutoStep();
      break;
    default:
      break;
  }
});
