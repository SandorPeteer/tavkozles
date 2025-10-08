// Kérdések adatbázisa
const questions = [
    // I. Wireless alapok, elektromágneses hullámok
    "Mi az elektromágneses sugárzás, és hogyan terjed?",
    "Mi a kapcsolat a hullámhossz és frekvencia között?",
    "Mit jelent a vezeték nélküli kommunikáció?",
    "Hogyan fedezték fel az elektromágneses hullámokat?",
    "Mely frekvenciák haladnak át a földi atmoszférán?",
    "Mik a különbségek a különböző frekvenciájú hullámok viselkedésében?",
    "Mitől függ, hogy egy hullám visszaverődik vagy áthalad egy tárgyon?",
    "Hogyan terjednek a rádióhullámok a Föld atmoszféráján belül és kívül?",
    "Az elektromágneses spektrum mely hullámhossz tartományába esik a látható fény?",
    "Melyik fénytartományt nem látjuk a szemünkkel, nevezd meg mind a kettőt?",
    "Milyen lehetőségek állnak rendelkezésre a vezeték nélküli kommunikációhoz? (mit használhatunk az elektromágneses hullám tartományaiból?)",
    "Milyen technológiával tudunk távolba küldeni információt?",
    "Milyen analóg modulációkat ismersz?",
    "Milyen digitális modulációkat ismersz?",
    "Mi az az antenna?",
    "Mi az izotróp antenna?",
    "Mi a sugárázási karakterisztika",
    "Mi az antenna nyeresége",
    "Mi az impedancia",
    "Számold ki egy 300MHz-en működő antenna negyed hullámhosszúságú fizikai méretét.",
    "Az 1 méter hosszú antenna milyen frekvencián üzemel?",
    "Milyen frekvenciasávot használ az FM műsorszórás?",
    "A monopól antenna milyen irányba sugároz?",
    "Sorolj fel néhány népszerű irányított antennát!",
    "Mikor megyünk haza?"
    

   
];

let currentQuestionIndex = 0;
let timeRemaining = 0;
let timer;
let selectedQuestions = [];
let answers = [];
let startTime, endTime;

const startSection = document.getElementById("start-section");
const quizSection = document.getElementById("quiz-section");
const endSection = document.getElementById("end-section");
const questionEl = document.getElementById("question");
const answerEl = document.getElementById("answer");
const timerEl = document.getElementById("timer");

document.addEventListener("DOMContentLoaded", () => {
    entryPoint();
});

// Main entry point of program
function entryPoint() {
    document.addEventListener("visibilitychange", handleVisibilityChange);
}

// Dolgozat vége, ha az oldal elhagyásra kerül
function handleVisibilityChange() {
    if (document.visibilityState === "hidden") {
        alert("Elhagytad az oldalt. A teszt véget ért számodra!");
        endQuiz(); // Hívjuk meg a teszt lezárására szolgáló függvényt
    }
}

// Remove visibility change event listener
function removeVisibilityChangeListener() {
    document.removeEventListener("visibilitychange", handleVisibilityChange);
}

document.getElementById("start-btn").addEventListener("click", () => {
    startTime = new Date(); // Aktuális kezdési idő
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!name || !email) {
        alert("Kérlek, add meg a neved és az email címed!");
        return;
    }

    startSection.style.display = "none";
    quizSection.style.display = "flex";

    selectedQuestions = questions.sort(() => 0.5 - Math.random()).slice(0, 10);
    startQuiz();
});

document.getElementById("back-btn").addEventListener("click", () => {
    // Remove visibility change eventlistener before redirect
    removeVisibilityChangeListener();
    // Átirányítás a főoldalra
    window.location.href = "https://sandorpeteer.github.io/tavkozles/";
});

function startQuiz() {
    currentQuestionIndex = 0;
    answers = [];
    showQuestion();
}

function showQuestion() {
    if (currentQuestionIndex >= selectedQuestions.length) {
        endQuiz();
        return;
    }

    questionEl.textContent = selectedQuestions[currentQuestionIndex];
    answerEl.value = "";
    setTimer(40 + selectedQuestions[currentQuestionIndex].length / 2); // Duplázott idő

    document.getElementById("next-btn").onclick = () => {
        saveAnswer();
        currentQuestionIndex++;
        showQuestion();
    };
}

function setTimer(seconds) {
    timeRemaining = Math.ceil(seconds);
    timerEl.textContent = `Válaszadási idő: ${timeRemaining} másodperc`;

    timer = setInterval(() => {
        timeRemaining--;
        timerEl.textContent = `Válaszadási idő: ${timeRemaining} másodperc`;

        if (timeRemaining <= 0) {
            clearInterval(timer);
            saveAnswer();
            currentQuestionIndex++;
            showQuestion();
        }
    }, 1000);
}

function saveAnswer() {
    clearInterval(timer);
    answers.push({
        question: selectedQuestions[currentQuestionIndex],
        answer: answerEl.value.trim() || "Nem érkezett válasz!"
    });
}

function endQuiz() {
    removeVisibilityChangeListener();

    startSection.style.display = "none";
    quizSection.style.display = "none";
    endSection.style.display = "flex";
    endTime = new Date(); // Aktuális befejezési idő
    sendEmail();
    document.getElementById("download-btn").addEventListener("click", downloadResults);
}

function downloadResults() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const timeTaken = calculateTimeTaken();
    let resultText = `Tanuló neve: ${name}\nEmail: ${email}\nTeszt kezdési idő: ${startTime}\nTeszt befejezési idő: ${endTime}\nTeszt kitöltési idő: ${timeTaken}\n\nVezeték nélküli adatátvitel Kérdések és válaszok:\n\n`;

    answers.forEach((a, index) => {
        resultText += `${index + 1}. Kérdés: ${a.question}\nVálasz: ${a.answer}\n\n`;
    });

    const blob = new Blob([resultText], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "vezeteknelkuli_dolgozat_letoltes.txt";
    link.click();
}

function sendEmail() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const teacherEmail = "pepe1125@gmail.com";
    const timeTaken = calculateTimeTaken();

    const message = `
        Tanuló neve: ${name}
        Tanuló email: ${email}
        Teszt kezdete: ${startTime}
        Teszt vége: ${endTime}
        Teszt kitöltési idő: ${timeTaken}

        Vezeték nélküli adatátvitel Kérdések és válaszok:
        ${answers.map(a => `Kérdés: ${a.question}\nVálasz: ${a.answer}\n`).join("\n")}
    `;

    emailjs.send("service_n5atsve", "template_lzmjifo", {
        to_email: teacherEmail,
        subject: name,
        reply_to: email,
        message: message
    }).then(() => {
        alert("Az eredményeket elküldtük SP tanárúrnak!");
    }).catch((error) => {
        console.error("Hiba az email küldésekor:", error);
        alert("Hiba történt az email küldésekor.");
    });
}

function calculateTimeTaken() {
    if (startTime && endTime) {
        const diff = endTime - startTime; // Különbség milliszekundumban
        const minutes = Math.floor(diff / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        return `${minutes} perc ${seconds} másodperc`;
    }
    return "Nincs adat";
}
