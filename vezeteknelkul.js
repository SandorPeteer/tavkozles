// Kérdések adatbázisa
const questions = [
    // I. Wireless alapok, elektromágneses hullámok
    "Mi az elektromágneses hullám, és hogyan terjed?",
    "Hogyan jellemezhető az elektromágneses hullám hullámhossza és frekvenciája?",
    "Mit jelent a vezeték nélküli kommunikáció?",
    "Hogyan fedezték fel az elektromágneses hullámokat?",
    "Milyen frekvenciák haladnak át a földi atmoszférán?",
    "Mik a különbségek a különböző frekvenciájú hullámok viselkedésében?",
    "Mitől függ, hogy egy hullám visszaverődik vagy áthalad egy tárgyon?",
    "Hogyan terjednek a rádióhullámok a Föld atmoszféráján belül és kívül?",

    // II. Adatátvitelre is alkalmas elektromágneses hullámok
    "Milyen hullámok alkalmasak adatátvitelre?",
    "Hogyan működik az infravörös kommunikáció?",
    "Mi az infravörös kommunikáció két fő alkalmazási módja?",
    "Miért nehéz a lézeres adatátvitelt lehallgatni?",
    "Milyen akadályok zavarhatják a lézeres adatátvitelt?",
    "Miért használunk mikrohullámokat adatátvitelre?",
    "Hogyan zavarhatja a mikrohullámú sütő a wifi működését?",
    "Mi az infrastruktúra típusú hálózat, és hogyan működik?",
    "Mi a különbség az ad-hoc és az infrastruktúra hálózat között?",
    "Hogyan működik a pont-pont adatkapcsolat kültéren?",

    // III. Kültéri rádiós link építhetőségét befolyásoló tényezők
    "Miért fontos a rálátás a kültéri rádiós linkeknél?",
    "Mi a Fresnel-zóna, és miért kell figyelembe venni?",
    "Mi történhet, ha a Fresnel-zónát akadályozzák?",
    "Hogyan befolyásolja a frekvencia a rádiós adatátvitel hatótávolságát?",
    "Milyen különbségek vannak a szabad és licencelt frekvenciasávok között?",
    "Miért nehéz nagy távolságú rádiós linkeket építeni magas frekvenciákon?",
    "Milyen problémákat okozhatnak a kültéri akadályok, például fák vagy épületek?",
    "Milyen gyakori telepítési hibák akadályozzák a kültéri rádiós linkek működését?",

    // Vegyesen még kérdések a tananyagból
    "Mi a vezeték nélküli kommunikáció lényege?",
    "Ki találta fel az elektromágneses hullámok elméletét?",
    "Mitől függ az elektromágneses hullám frekvenciája?",
    "Milyen hullámok haladnak át a földi atmoszférán?",
    "Hogyan használjuk az infravörös adatátvitelt?",
    "Mi zavarhatja a lézeres adatátvitelt?",
    "Milyen előnyei és hátrányai vannak a mikrohullámú adatátvitelnek?",
    "Mit jelent az ad-hoc hálózat?",
    "Mi a különbség az infrastruktúra és az ad-hoc hálózat között?",
    "Hogyan működik a pont-pont kapcsolat?",
    "Miért fontos a rálátás a kültéri linkeknél?",
    "Mi az a Fresnel-zóna, és miért számít?",
    "Miért csillapodik a jel a távolság növekedésével?",
    "Mi a különbség a szabad és licencelt frekvenciasávok között?",
    "Mitől függ egy antenna teljesítménye?",
    "Hogyan működik a körsugárzó antenna?",
    "Mit jelent az antenna nyeresége?",
    "Milyen helyzetekben használunk szektorantennát?",
    "Mire jó a parabolaantenna?",
    "Miért fontos az antenna pontos beállítása?",
    "Mit okoz az interferencia a rádiós adatátvitelnél?",
    "Hogyan választható interferenciamentes csatorna?",
    "Miért fontos a jelerősség a rádiós linkeknél?",
    "Mire jó a 802.11b és 802.11g szabvány?",
    "Hol használjuk az 5 GHz-es frekvenciát?",
    "Mi a MIMO technológia lényege?",
    "Miért előnyös az 5 GHz-es sáv?",
    "Mi határozza meg a rádiós link távolságát?",
    "Milyen antennát érdemes használni egy rádiós linkhez?",
    "Milyen problémákat okoz a szél egy kültéri antennánál?",
    "Hogyan hat az átfedő csatornák használata a hálózatra?",
    "Mi a különbség a pont-pont és a pont-multipont kapcsolat között?",
    "Mi zavarhatja a lézeres adatátvitelt, például napsütés?",
    "Miért fontos figyelembe venni a szabadtéri csillapítást?",
    "Hogyan segít a rádiós eszköz szoftvere az antenna beállításában?",
    "Milyen előnyei vannak a licencelt sávoknak?",
    "Mi a szerepe az Access Pointnak a hálózatban?",
    "Miért csökken az adatátviteli sebesség interferencia miatt?",
    "Hogyan lehet elkerülni az interferenciát?",
    "Mit jelent az antenna horizontális és vertikális nyílásszöge?",
    "Miért kell terhelés mellett állítani az antennákat?",
    "Hogyan jellemezhetjük egy rádiós link minőségét?",
    "Miért fontos a Data Rate az adatátvitelnél?",
    "Milyen különbség van az 5 GHz és a 2,4 GHz között?",
    "Miért lényeges a Fresnel-zóna tisztasága?",
    "Milyen sebességeket érhetünk el a 802.11ac szabvánnyal?",
    "Hogyan javítja az eszköz érzékenysége az adatátvitelt?"
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