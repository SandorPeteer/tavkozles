// Kérdések adatbázisa
const questions = [
    "Mi az interferencia, és mikor fordul elő?",
    "Milyen színekre érzékeny a szemünk?",
    "Hogyan terjed a fény különböző anyagokban?",
    "Mi a látható fény spektrumán kívüli két fény neve?",
    "Miért törik meg a fény, ha másik anyagba lép?",
    "Hogyan alakul ki a szivárvány?",
    "Mit nevezünk polarizált fénynek, és hol találkozunk vele?",
    "Miért látunk színeket különböző hullámhosszoknál?",
    "Hogyan érzékeli a fényt a szemünk?",
    "Hogyan függ össze a hullámhossz, a frekvencia és a fény sebessége?",
    "Mi a kapcsolat a frekvencia és a hang irányítottsága között? Miért irányítottabb egy 20 kHz-es hang, mint egy 20 Hz-es?",
    "Hogyan alakítjuk át a hanghullámot elektronikus jellé, és az elektronikus jelet újra hanghullámmá?",
    "A beszéd frekvenciája melyik tartományba esik a spektrumban?",
    "Hogyan történik az analóg jelek digitalizálása, és hogyan alakítjuk vissza őket számunkra érthető formába?",
    "Milyen előnyei vannak a digitális jeleknek az analóg jelekkel szemben?",
    "Milyen frekvenciatartományokat használhatunk vezeték nélküli távközlésre?",
    "Sorolj fel néhány modulációs típust!",
    "Milyen frekvenciatartományban sugároz az FM rádió?",
    "Milyen frekvenciatartományban működik a DVB-T Magyarországon? Hová esik a spektrumban?",
    "Miért kell tömöríteni a jeleket, és milyen tömörítési módszerek léteznek?",
    "Mondj példát veszteséges és veszteségmentes tömörítési eljárásokra hang esetében!",
    "Milyen tömörítési eljárásokat használunk fényképek esetében? Mondj egy példát veszteségesre és veszteségmentesre!",
    "Hogyan tömörítjük a mozgóképet, és miért van erre szükség? Mondj példát egy népszerű eljárásra!",
    "Milyen képarányok léteznek a videók esetében? Sorolj fel legalább kettőt!",
    "Milyen fps szabványokat ismerünk videókra?",
    "Melyek a legnépszerűbb videofelbontások? Sorolj fel legalább kettőt!",
    "Milyen modulációs eljárással érhetjük el, hogy egyidőben több információt tudjunk továbbítani egy csatornán?",
    "Mi a QAM moduláció, és hogyan növeli az adatátviteli kapacitást?",
    "Hogyan működik az OFDM (Orthogonal Frequency Division Multiplexing), és miért előnyös a műsorszórásban?",
    "Mit nevezünk multiplexálásnak, és hogyan alkalmazzák a műsorszórásban?",
    "Hogyan lehet egyszerre több szimbólumot továbbítani egyetlen hullámon?",
    "Milyen modulációs típusokat használnak a digitális földfelszíni televíziózásban (DVB-T)?",
    "Mi a különbség az analóg és digitális modulációs technikák között a műsorszórásban?",
    "Hogyan csökkenti az OFDM az interferencia hatásait a műsorszórás során?",
    "Mi az FDM (Frequency Division Multiplexing), és hogyan használják a rádiós műsorszórásban?",
    "Mit jelent az, hogy egy moduláció nagyobb spektrális hatékonyságot biztosít?",
    "Hogyan osztja szét az információt a DVB-T2 szabvány több vivőfrekvencián keresztül?",
    "Miért fontos a hibajavító kódolás a műsorszórásban, és hogyan javítja a vétel minőségét?",
    "Hogyan használja a DVB-T a COFDM (Coded Orthogonal Frequency Division Multiplexing) technológiát?",
    "Miért használják a kvadratúra amplitúdó modulációt (QAM) a digitális televíziózásban?",
    "Milyen előnyei vannak a digitális modulációnak az analóggal szemben a műsorszórás során?"
];

let currentQuestionIndex = 0;
let timeRemaining = 0;
let timer;
let selectedQuestions = [];
let answers = [];

const startSection = document.getElementById("start-section");
const quizSection = document.getElementById("quiz-section");
const endSection = document.getElementById("end-section");
const questionEl = document.getElementById("question");
const answerEl = document.getElementById("answer");
const timerEl = document.getElementById("timer");

// Dolgozat vége, ha az oldal elhagyásra kerül
document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") {
        alert("Elhagytad az oldalt. A teszt véget ért számodra!");
        endQuiz(); // Hívjuk meg a teszt lezárására szolgáló függvényt
    }
});

document.getElementById("start-btn").addEventListener("click", () => {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!name || !email) {
        alert("Kérlek, add meg a neved és az email címed!");
        return;
    }

    startSection.classList.add("hidden");
    quizSection.classList.remove("hidden");

    selectedQuestions = questions.sort(() => 0.5 - Math.random()).slice(0, 10);
    startQuiz();
});

document.getElementById("back-btn").addEventListener("click", () => {
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
    quizSection.classList.add("hidden");
    endSection.classList.remove("hidden");
    sendEmail();
    document.getElementById("download-btn").addEventListener("click", downloadResults);
}

function downloadResults() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    let resultText = `Tanuló neve: ${name}\nEmail: ${email}\n\nKérdések és válaszok:\n`;

    answers.forEach((a, index) => {
        resultText += `${index + 1}. Kérdés: ${a.question}\nVálasz: ${a.answer}\n\n`;
    });

    const blob = new Blob([resultText], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "musorszoro_dolgozat_letoltes.txt";
    link.click();
}

function sendEmail() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const teacherEmail = "pepe1125@gmail.com";

    const message = `
                        Tanuló neve: ${name}
                        Tanuló email: ${email}
                        
                        Kérdések és válaszok:
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
