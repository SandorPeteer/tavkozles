// Kérdések adatbázisa
const questions = [
// II. Közeghozzáférés, CSMA/CA és Wi-Fi specifikumok
    "Miért van szükség közeghozzáférési metódusokra (pl. CSMA/CA) a vezeték nélküli hálózatokban, és mi történik ezek hiányában?",
    "Melyek a CSMA/CA (Carrier Sense Multiple Access / Collision Avoidance) eljárás működésének főbb lépései a 802.11 szabvány szerint?",
    "Mi a magyarázata annak, hogy a 802.11 szabványoknál a valós, kimérhető átviteli sebesség jelentősen elmarad az elméleti Data Rate-től?",
    "Mit jelent a \"rejtett node\" (hidden node) probléma a Wi-Fi hálózatokban?",
    "Milyen mechanizmussal oldható meg a rejtett csomópont probléma a 802.11 hálózatokban, és hogyan működik ez az eljárás?",
    "Milyen közeghozzáférési módot használnak a modern, nagy teljesítményű kültéri rádiós protokollok a CSMA/CA helyett, és mi ennek a működési elve?",
    "Mi a különbség a 2,4 GHz-es és az 5 GHz-es frekvenciasáv között a jel csillapodása tekintetében?",
    "Mi az interferencia fizikai jelensége, és milyen konkrét hatással van a digitálisan modulált vezeték nélküli adatátvitelre?"
   
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
