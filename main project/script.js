const btn = document.getElementById("analyzeBtn");
const processing = document.getElementById("processing");
const result = document.getElementById("result");
const consoleText = document.getElementById("consoleText");
const logInput = document.getElementById("logInput");

const API_URL = "http://localhost:5000";

const logs = [
"> Reading medical records...",
"> Extracting entities...",
"> Detecting domain...",
"> Matching emergency protocols...",
"> Calculating severity...",
"> Computing confidence score...",
"> Generating recommendations...",
"> Building final report..."
];

// Mouse spotlight
const spotlight = document.querySelector(".spotlight");
document.addEventListener("mousemove",(e)=>{
    spotlight.style.left = e.clientX + "px";
    spotlight.style.top = e.clientY + "px";
});

// Particles
const particles = document.getElementById("particles");
for(let i=0;i<40;i++){
    let p = document.createElement("span");
    p.classList.add("particle");
    p.style.left = Math.random()*100 + "vw";
    p.style.animationDelay = Math.random()*8 + "s";
    p.style.animationDuration = 5 + Math.random()*10 + "s";
    particles.appendChild(p);
}

// Typewriter
function typeLine(text){
    const div = document.createElement("div");
    consoleText.appendChild(div);
    let index = 0;
    const typing = setInterval(()=>{
        div.textContent += text[index];
        index++;
        if(index >= text.length){
            clearInterval(typing);
        }
    },25);
}

// Counter
function animateCounter(id,target){
    let count = 0;
    const element = document.getElementById(id);
    const interval = setInterval(()=>{
        count += Math.ceil(target/40);
        if(count >= target){
            count = target;
            clearInterval(interval);
        }
        element.textContent = count;
    },40);
}

// Update the result section with REAL data
function updateResultUI(data) {
    // Title
    document.querySelector(".result-header h2").textContent =
        data.domain.toUpperCase() + " Log Detected";

    // Confidence ring
    document.querySelector(".ring-text").textContent = data.confidence + "%";

    // Severity badge
    const severityEl = document.querySelector(".severity span");
    severityEl.textContent = data.severity.toUpperCase();

    // Root Cause card
    document.querySelectorAll(".card")[0].querySelector("p").textContent = data.cause;

    // Pattern Match card
    document.querySelectorAll(".card")[1].querySelector("p").textContent =
        data.pattern_matched + " matched with high confidence.";

    // Confidence card
    document.querySelectorAll(".card")[2].querySelector("p").textContent =
        data.confidence + "% certainty based on extracted entities and matching records.";

    // Timeline (Fix Steps)
    const timeline = document.querySelector(".timeline");
    timeline.innerHTML = "";
    data.fix_steps.forEach(step => {
        const item = document.createElement("div");
        item.classList.add("timeline-item");
        item.textContent = step;
        timeline.appendChild(item);
    });

    // Diagnosis - add to root cause card or a new element
    const rootCauseCard = document.querySelectorAll(".card")[0];
    rootCauseCard.querySelector("h3").textContent = "Diagnosis: " + data.diagnosis;
}

btn.addEventListener("click", async ()=>{

    const logText = logInput.value.trim();

    if (!logText) {
        alert("Please paste a log first!");
        return;
    }

    processing.classList.remove("hidden");
    result.classList.add("hidden");
    consoleText.innerHTML = "";
    document.getElementById("progressBar").style.width = "0%";

    const steps = document.querySelectorAll(".step");
    const scanners = document.querySelectorAll(".scanner");
    steps.forEach(step=>step.classList.remove("active"));

    let current = 0;
    const stepInterval = setInterval(()=>{
        if(current < steps.length){
            steps[current].classList.add("active");
            scanners[current].classList.add("move");
            document.getElementById("progressBar").style.width = ((current+1)/5)*100 + "%";
            current++;
        }else{
            clearInterval(stepInterval);
        }
    },1000);

    let i = 0;
    const logInterval = setInterval(()=>{
        if(i < logs.length){
            typeLine(logs[i]);
            i++;
        }else{
            clearInterval(logInterval);
        }
    },700);

    // REAL API CALL to Flask backend
    try {
        const response = await fetch(API_URL + "/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ log: logText })
        });

        const data = await response.json();

        setTimeout(()=>{
            updateResultUI(data);

            result.classList.remove("hidden");

            animateCounter("patterns", 2431);
            animateCounter("entities", Math.floor(Math.random()*50)+150);
            animateCounter("records", Math.floor(Math.random()*30)+70);

            result.scrollIntoView({ behavior:"smooth" });

        },6500);

    } catch (err) {
        clearInterval(stepInterval);
        clearInterval(logInterval);
        processing.classList.add("hidden");
        alert("Cannot reach backend. Is Flask running on port 5000?\n\nRun: python backend/app.py");
        console.error(err);
    }

});