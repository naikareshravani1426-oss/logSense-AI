const btn = document.getElementById("analyzeBtn");
const processing = document.getElementById("processing");
const result = document.getElementById("result");
const consoleText = document.getElementById("consoleText");

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

btn.addEventListener("click",()=>{

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

            document.getElementById("progressBar")
            .style.width = ((current+1)/5)*100 + "%";

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

    setTimeout(()=>{

        result.classList.remove("hidden");

        animateCounter("patterns",2431);
        animateCounter("entities",184);
        animateCounter("records",91);

        result.scrollIntoView({
            behavior:"smooth"
        });

    },6500);

});