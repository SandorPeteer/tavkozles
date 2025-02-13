// Kérdések adatbázisa
const questions = [
    // Frekvenciasávok és cellás felépítés
    "Milyen frekvenciatartományban működik a GSM uplink (UL) irányban?",
    "Mi a GSM downlink (DL) frekvenciatartománya?",
    "Mekkora sávszélességet használ a GSM rendszer, és hány vivőre oszlik?",
    "Hogyan biztosítja a GSM rendszer a frekvenciák újrafelhasználását (Frequency Reuse Factor)?",
    "Hová helyezik a cellák antennáit, és miért irányított a sugárzásuk?",

    // Időalapú multiplexálás (TDMA)
    "Mi az időalapú multiplexálás (TDMA), és hogyan működik a GSM-ben?",
    "Hány időrés (timeslot) van egy vivőn, és egy időrés milyen hosszú?",
    "Mennyi adatot továbbít egy GSM időrés 20 ms alatt?",

    // Adattömörítés és hibajavítás
    "Milyen mintavételezési frekvenciát használ a GSM kodek?",
    "Mi a hibajavító kódok (ECC) szerepe a GSM rendszerben?",
    "Mekkora az adatsebesség a GSM Full Rate (FR) és Half Rate (HR) esetében?",

    // Beszédtömörítés és háttérzaj kezelés
    "Mi a Voice Activity Detection (VAD) funkciója a GSM hálózatban?",
    "Mit jelent a Comfort Noise Generation (CNG), és hogyan javítja a beszédélményt?",

    // Moduláció és frekvencia kezelés
    "Mi az a GMSK (Gaussian Minimum Shift Keying), és miért alkalmazza a GSM?",
    "Hogyan működik a Frequency Hopping, és miért fontos a GSM hálózatban?",
    "Miért használ a GSM hálózat N=12 elosztást a Frequency Reuse Factor esetében?",

    // Azonosítás és biztonság
    "Mit azonosít az IMEI a GSM rendszerben?",
    "Mi az IMSI, és hogyan különbözik az MSISDN-től?",
    "Mit jelent a TMSI, és hogyan védi a felhasználókat?",
    "Mi a hitelesítés (authentication) szerepe a GSM hálózatban?",
    "Hogyan biztosítja a GSM rendszer a kommunikáció titkosítását?",

    // GSM hálózati architektúra
    "Mit tárol a HLR (Home Location Register), és mi a szerepe?",
    "Mi a VLR (Visitor Location Register) funkciója?",
    "Mi a MSC (Mobile Switching Center) fő feladata a GSM hálózatban?",
    "Milyen feladatokat lát el az AUC (Authentication Center)?",
    "Hogyan működik az EIR (Equipment Identity Register), és miért fontos?",
    "Mit csinál az SMSC (Short Message Service Center)?",
    "Mi a BSC (Base Station Controller) és a BTS (Base Transceiver Station) szerepe a GSM rendszerben?",

    // Hálózat működése
    "Hogyan kapcsolódnak egymáshoz a HLR, VLR és MSC elemek a híváskezelés során?",
    "Mit jelent az O&M (Operation and Maintenance) rendszer, és miért szükséges?",
    "Miért fontos a Billing/Charging rendszer a GSM hálózatban?",

    // Hálózat fejlődése
    "Milyen frekvenciasávban működtek az analóg NMT rendszerek Magyarországon?",
    "Miért volt áttörés a digitális 2G rendszer a mobilkommunikációban?",
    "Hogyan biztosítja a GSM hálózat a felhasználók mobilitását mozgás közben?"
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
    let resultText = `Tanuló neve: ${name}\nEmail: ${email}\nTeszt kezdési idő: ${startTime}\nTeszt befejezési idő: ${endTime}\nTeszt kitöltési idő: ${timeTaken}\n\nMobil távközlés Kérdések és válaszok:\n\n`;

    answers.forEach((a, index) => {
        resultText += `${index + 1}. Kérdés: ${a.question}\nVálasz: ${a.answer}\n\n`;
    });

    const blob = new Blob([resultText], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "mobil_tavkozl_dolgozat_letoltes.txt";
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
        
                        Mobil távközlés Kérdések és válaszok:
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
