Rendben, részletesen kidolgozom a teljes projektet, beleértve az adatbázis létrehozását, néhány minta kérdés hozzáadását, valamint a webalkalmazás kliensoldali (frontend) részének megírását. Az alkalmazás ASP.NET Core MVC keretrendszeren alapul, Entity Framework Core segítségével kommunikál a MySQL adatbázissal, és Swaggerrel biztosítja az API dokumentációt.

Tartalomjegyzék
	1.	Adatbázis Felépítése
	•	Adatbázis és Táblák Létrehozása
	•	Minta Kérdések Hozzáadása
	2.	ASP.NET Core Projekt Beállítása
	•	Projekt Létrehozása
	•	NuGet Csomagok Telepítése
	3.	Modellek Generálása az Adatbázisból
	•	Scaffolding Használata
	4.	Swagger Integrálása
	5.	QuizController és Nézetek Létrehozása
	•	QuizController.cs
	•	ViewModels Létrehozása
	•	Nézetek Létrehozása
	6.	Eredmények Titkosítása és Email Küldése
	•	Titkosítási Kulcs Beállítása
	•	Email Küldési Funkció Implementálása
	7.	Biztonsági Intézkedések
	8.	Teljes Projekt Összefoglalása
	9.	Záró Gondolatok

Adatbázis Felépítése

Adatbázis és Táblák Létrehozása

Először is létre kell hoznunk a testapi nevű adatbázist és a szükséges táblákat. Használd a következő SQL parancsokat a phpMyAdmin felületén:

-- Adatbázis létrehozása
CREATE DATABASE IF NOT EXISTS testapi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE testapi;

-- Kérdések táblája
CREATE TABLE IF NOT EXISTS Questions (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Content TEXT NOT NULL,
    OptionA VARCHAR(255) NOT NULL,
    OptionB VARCHAR(255) NOT NULL,
    OptionC VARCHAR(255) NOT NULL,
    OptionD VARCHAR(255) NOT NULL,
    CorrectOption VARCHAR(1) NOT NULL,
    Complexity INT NOT NULL
);

-- Felhasználói válaszok táblája
CREATE TABLE IF NOT EXISTS UserResponses (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    QuestionId INT NOT NULL,
    SelectedOption VARCHAR(1) NOT NULL,
    TimeTaken TIME NOT NULL,
    FOREIGN KEY (QuestionId) REFERENCES Questions(Id)
);

-- Teszt eredmények táblája
CREATE TABLE IF NOT EXISTS TestResults (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    CompletedAt DATETIME NOT NULL,
    EncryptedData TEXT NOT NULL
);

Minta Kérdések Hozzáadása

Töltsünk fel néhány minta kérdést a Questions táblába:

INSERT INTO Questions (Content, OptionA, OptionB, OptionC, OptionD, CorrectOption, Complexity) VALUES
('Melyik a leggyakrabban használt vezeték nélküli kommunikációs technológia rövid távolságra?', 'Bluetooth', 'Ethernet', 'USB', 'HDMI', 'A', 2),
('Mi az OFDM (Orthogonal Frequency Division Multiplexing) fő előnye a távközlésben?', 'Adat tömörítés', 'Interferencia csökkentése', 'Frekvencia szétválasztás', 'Jelátvitel', 'C', 3),
('Melyik eszköz felelős a Wi-Fi jel erősítéséért és kiterjesztéséért?', 'Router', 'Modem', 'Repeater', 'Switch', 'C', 2),
('Mi a fő funkciója az SDN (Software Defined Networking) technológiának?', 'Hardveres eszközök vezérlése', 'Szoftveres útválasztás és hálózatirányítás', 'Adat tömörítés', 'Jelátvitel', 'B', 4),
('Melyik protokoll felelős az IP-címek kiosztásáért a hálózatban?', 'HTTP', 'FTP', 'DHCP', 'SMTP', 'C', 2),
('Mi az 5G technológia egyik kulcsfontosságú jellemzője a távközlésben?', 'Alacsony sebesség', 'Nagy sávszélesség', 'Csak vezetékes kapcsolatok', 'Csak rövid távolságokra alkalmazható', 'B', 3),
('Melyik távközlési technológia használatos a műholdas kommunikációban?', 'Fiber optika', 'Radiofrekvenciák', 'Bluetooth', 'Ethernet', 'B', 4),
('Mi a célja a MIMO (Multiple Input Multiple Output) technológiának a vezeték nélküli kommunikációban?', 'Adat biztonság növelése', 'Több csatorna párhuzamos használata a sebesség növelésére', 'Energiafogyasztás csökkentése', 'Jel zaj csökkentése', 'B', 3),
('Melyik a legelterjedtebb vezeték nélküli hálózati szabvány?', 'IEEE 802.11', 'IEEE 802.3', 'IEEE 802.15', 'IEEE 802.16', 'A', 2),
('Mi a fő különbség a 4G és az 5G hálózatok között?', 'Csak a sebesség különbözik', 'Az 5G több sávszélességet és alacsonyabb késleltetést kínál', 'A 4G használ nem digitális jeleket', 'A 5G csak vezetékes hálózatokra érvényes', 'B', 3);

Magyarázat a Kérdésekhez:
	1.	Bluetooth: Rövid távú vezeték nélküli kommunikációra használatos.
	2.	OFDM: Hatékony frekvenciafelhasználást és interferencia csökkentést tesz lehetővé.
	3.	Repeater: Növeli a Wi-Fi jel terjedési távolságát.
	4.	SDN: Szoftveres útválasztás és hálózatirányítás.
	5.	DHCP: Automatikusan kiosztja az IP-címeket.
	6.	5G: Nagy sávszélességet és alacsony késleltetést kínál.
	7.	Radiofrekvenciák: Műholdas kommunikációban használatosak.
	8.	MIMO: Több antennán keresztül növeli a kommunikációs sebességet.
	9.	IEEE 802.11: Legelterjedtebb Wi-Fi szabvány.
	10.	4G vs 5G: Az 5G több sávszélességet és alacsonyabb késleltetést kínál.

ASP.NET Core Projekt Beállítása

Projekt Létrehozása
	1.	Visual Studio Megnyitása:
	•	Indítsd el a Visual Studio-t.
	•	Válaszd a Create a new project opciót.
	2.	Projekt Típusa:
	•	Válaszd az ASP.NET Core Web App (Model-View-Controller) sablont.
	•	Kattints a Next gombra.
	3.	Projekt Neve és Helye:
	•	Nevezd el a projektet TelecomQuizApp-nak.
	•	Válaszd ki a megfelelő helyet a projekt mentéséhez.
	•	Kattints a Create gombra.
	4.	Framework Kiválasztása:
	•	Válaszd ki a .NET 6.0 vagy későbbi verziót.
	•	Kattints a Create gombra.

NuGet Csomagok Telepítése

Nyisd meg a NuGet Package Manager Console-t (Tools > NuGet Package Manager > Package Manager Console) és futtasd a következő parancsokat:

Install-Package Pomelo.EntityFrameworkCore.MySql
Install-Package Microsoft.EntityFrameworkCore.Tools
Install-Package Swashbuckle.AspNetCore
Install-Package MailKit
Install-Package Microsoft.AspNetCore.Session

Csomagok Magyarázata:
	•	Pomelo.EntityFrameworkCore.MySql: MySQL támogatást nyújt az Entity Framework Core számára.
	•	Microsoft.EntityFrameworkCore.Tools: Eszközök az EF Core-hoz (pl. migrációkhoz).
	•	Swashbuckle.AspNetCore: Swagger integrálása az ASP.NET Core projekthez.
	•	MailKit: Emailek küldéséhez szükséges könyvtár.
	•	Microsoft.AspNetCore.Session: Szekció kezeléshez.

Modellek Generálása az Adatbázisból

Scaffolding Használata

Az Entity Framework Core lehetővé teszi, hogy a meglévő adatbázisból generáljunk modelleket és a DbContext osztályt. Ehhez a Scaffold-DbContext parancsot használjuk.
	1.	Connection String Beállítása:
Nyisd meg az appsettings.json fájlt és győződj meg róla, hogy a következő beállítás szerepel:

{
  "ConnectionStrings": {
    "DefaultConnection": "server=localhost;database=testapi;user=root;password=password;SslMode=None;"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}

Fontos: Cseréld ki a password részt a MySQL root felhasználó jelszavára vagy arra a felhasználóra, amelyet az alkalmazás használ.

	2.	Modellek és DbContext Generálása:
A Package Manager Console-ban navigálj a projekt könyvtárába és futtasd a következő parancsot:

Scaffold-DbContext "server=localhost;database=testapi;user=root;password=password;SslMode=None;" Pomelo.EntityFrameworkCore.MySql -OutputDir Models -Context ApplicationDbContext -Force

Paraméterek Magyarázata:
	•	Connection String: Megadja a kapcsolatot a MySQL adatbázissal.
	•	Provider: Pomelo.EntityFrameworkCore.MySql
	•	Output Directory: A generált modellek a Models mappába kerülnek.
	•	DbContext Név: ApplicationDbContext
	•	Force: Felülírja a meglévő fájlokat, ha vannak.

	3.	Generált Fájlok Ellenőrzése:
A parancs futtatása után a Models mappában megtalálhatók a generált osztályok:
	•	Question.cs
	•	UserResponse.cs
	•	TestResult.cs
	•	ApplicationDbContext.cs
Ezek az osztályok megfelelnek az adatbázis tábláinak és azok mezőinek.

Swagger Integrálása

A Swagger segítségével automatikusan generálhatunk interaktív API dokumentációt, amely megkönnyíti az API-k tesztelését és megértését.

Swagger Beállítása
	1.	Program.cs Módosítása:
Nyisd meg a Program.cs fájlt, és add hozzá a Swagger szolgáltatások regisztrálását és a middleware beállítását.

using Microsoft.EntityFrameworkCore;
using TelecomQuizApp.Data;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Entity Framework konfigurálása MySQL-lel
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));

// Session konfigurálása
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// Swagger szolgáltatások hozzáadása
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "TelecomQuiz API",
        Version = "v1",
        Description = "API dokumentáció a TelecomQuiz alkalmazáshoz"
    });

    // Opció: XML dokumentáció engedélyezése (ha van)
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        c.IncludeXmlComments(xmlPath);
    }
});

var app = builder.Build();

// HTTP request pipeline konfigurálása
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// Swagger middleware hozzáadása (fejlesztési környezetben)
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "TelecomQuiz API V1");
        c.RoutePrefix = "swagger"; // Elérhetőség: https://localhost:<port>/swagger
    });
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

// Session használata
app.UseSession();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Quiz}/{action=Start}/{id?}");

app.Run();


	2.	XML Dokumentáció Engedélyezése (Opció):
Ha szeretnél részletesebb dokumentációt generálni, engedélyezheted az XML kommentárokat.
	•	Projekt Beállítása:
	•	Kattints a projekt nevére a Solution Explorer-ben.
	•	Válaszd a Properties lehetőséget.
	•	Navigálj a Build fülre.
	•	Pipáld be az XML documentation file opciót, és adj meg egy elérési utat, például bin\Debug\net6.0\TelecomQuizApp.xml.
	•	Swagger Konfiguráció Frissítése:
A Program.cs-ben már hozzáadtuk az XML dokumentáció beillesztését, ha létezik.

QuizController és Nézetek Létrehozása

QuizController.cs

Hozz létre egy új kontrollert Controllers/QuizController.cs néven, amely kezeli a quiz folyamatát: kezdés, kérdések megjelenítése, válaszok rögzítése, eredmények tárolása és email küldése.

using Microsoft.AspNetCore.Mvc;
using TelecomQuizApp.Data;
using TelecomQuizApp.Models;
using TelecomQuizApp.ViewModels;
using System.Threading.Tasks;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using MimeKit;
using MailKit.Net.Smtp;

namespace TelecomQuizApp.Controllers
{
    public class QuizController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        public QuizController(ApplicationDbContext context, IConfiguration configuration)
        {
            _context = context;
            _configuration = configuration;
        }

        // GET: Quiz/Start
        public IActionResult Start()
        {
            return View();
        }

        // POST: Quiz/Start
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Start(UserInfoViewModel model)
        {
            if (ModelState.IsValid)
            {
                // Felhasználói információk tárolása session-ben
                HttpContext.Session.SetString("UserName", model.UserName);
                HttpContext.Session.SetString("Email", model.Email);
                // Inicializáljuk az answeredQuestions listát
                HttpContext.Session.SetString("AnsweredQuestions", JsonSerializer.Serialize(new List<QuestionViewModel>()));
                return RedirectToAction("Quiz");
            }
            return View(model);
        }

        // GET: Quiz/Quiz
        public async Task<IActionResult> Quiz()
        {
            // Ellenőrizzük, hogy a felhasználói adatok elérhetőek-e
            var userName = HttpContext.Session.GetString("UserName");
            var email = HttpContext.Session.GetString("Email");

            if (string.IsNullOrEmpty(userName) || string.IsNullOrEmpty(email))
            {
                return RedirectToAction("Start");
            }

            // Lekérjük a már válaszolt kérdéseket
            var answeredQuestionsJson = HttpContext.Session.GetString("AnsweredQuestions");
            var answeredQuestions = JsonSerializer.Deserialize<List<QuestionViewModel>>(answeredQuestionsJson);

            if (answeredQuestions.Count >= 10)
            {
                // Quiz befejezve
                return RedirectToAction("Result");
            }

            // Véletlenszerűen kiválasztunk egy kérdést, amit még nem válaszoltak meg
            var unansweredQuestions = _context.Questions.Where(q => !answeredQuestions.Any(aq => aq.QuestionId == q.Id)).ToList();

            if (!unansweredQuestions.Any())
            {
                // Nincs több kérdés, de a kérdések száma nem éri el a 10-et
                // Itt kezelhetjük, például új kérdéseket adhatsz hozzá
                return RedirectToAction("Result");
            }

            var random = new Random();
            var question = unansweredQuestions[random.Next(unansweredQuestions.Count)];

            // Idő kalkulálása a komplexitás alapján (pl. 30 másodperc per komplexitási szint)
            int timeAllocated = question.Complexity * 30;

            var viewModel = new QuestionViewModel
            {
                QuestionId = question.Id,
                Content = question.Content,
                OptionA = question.OptionA,
                OptionB = question.OptionB,
                OptionC = question.OptionC,
                OptionD = question.OptionD,
                TimeAllocated = timeAllocated,
                CurrentQuestionNumber = answeredQuestions.Count + 1
            };

            return View(viewModel);
        }

        // POST: Quiz/Quiz
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Quiz(QuestionViewModel model)
        {
            if (ModelState.IsValid)
            {
                // Lekérjük a már válaszolt kérdéseket
                var answeredQuestionsJson = HttpContext.Session.GetString("AnsweredQuestions");
                var answeredQuestions = JsonSerializer.Deserialize<List<QuestionViewModel>>(answeredQuestionsJson);

                // Rögzítjük az aktuális választ
                answeredQuestions.Add(new QuestionViewModel
                {
                    QuestionId = model.QuestionId,
                    SelectedOption = model.SelectedOption,
                    TimeTaken = model.TimeTaken,
                    // Optionálisan: Complexity, stb.
                });

                // Frissítjük a session-t
                HttpContext.Session.SetString("AnsweredQuestions", JsonSerializer.Serialize(answeredQuestions));

                if (answeredQuestions.Count >= 10)
                {
                    // Quiz befejezve
                    return RedirectToAction("Result");
                }

                return RedirectToAction("Quiz");
            }

            return View(model);
        }

        // GET: Quiz/Result
        public async Task<IActionResult> Result()
        {
            var userName = HttpContext.Session.GetString("UserName");
            var email = HttpContext.Session.GetString("Email");
            var answeredQuestionsJson = HttpContext.Session.GetString("AnsweredQuestions");
            var answeredQuestions = JsonSerializer.Deserialize<List<QuestionViewModel>>(answeredQuestionsJson);

            if (string.IsNullOrEmpty(userName) || string.IsNullOrEmpty(email) || answeredQuestions == null)
            {
                return RedirectToAction("Start");
            }

            // Generáljuk az eredmény adatokat és titkosítjuk
            var encryptedData = EncryptResults(answeredQuestions, userName, email);

            // Mentjük az eredményt az adatbázisba
            var testResult = new TestResult
            {
                UserName = userName,
                Email = email,
                CompletedAt = DateTime.UtcNow,
                EncryptedData = encryptedData
            };

            _context.TestResults.Add(testResult);
            await _context.SaveChangesAsync();

            // Töröljük a session adatokat
            HttpContext.Session.Clear();

            return View(testResult);
        }

        // POST: Quiz/SendResult
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SendResult(int TestResultId)
        {
            var testResult = await _context.TestResults.FindAsync(TestResultId);
            if (testResult == null)
            {
                return NotFound();
            }

            // Email összeállítása
            var message = new MimeMessage();
            message.From.Add(new MailboxAddress("Quiz Rendszer", _configuration["SmtpSettings:SenderEmail"]));
            message.To.Add(new MailboxAddress(testResult.UserName, testResult.Email));
            message.Subject = "A Quiz Eredményei";

            var body = new TextPart("plain")
            {
                Text = "Köszönjük a részvételt a quizben. Az eredményeidet titkosítva csatoltad."
            };

            // Titkosított adat csatolása szövegfájlként
            var attachment = new MimePart("text", "plain")
            {
                Content = new MimeContent(new MemoryStream(Encoding.UTF8.GetBytes(testResult.EncryptedData)), ContentEncoding.Default),
                ContentDisposition = new ContentDisposition(ContentDisposition.Attachment),
                ContentTransferEncoding = ContentEncoding.Base64,
                FileName = $"QuizResult_{testResult.Id}.txt"
            };

            var multipart = new Multipart("mixed");
            multipart.Add(body);
            multipart.Add(attachment);

            message.Body = multipart;

            // Email küldése
            using (var client = new SmtpClient())
            {
                // Biztonsági okokból minden SSL tanúsítványt elfogadunk
                client.ServerCertificateValidationCallback = (s, c, h, e) => true;

                await client.ConnectAsync(_configuration["SmtpSettings:Server"], int.Parse(_configuration["SmtpSettings:Port"]), MailKit.Security.SecureSocketOptions.StartTls);
                await client.AuthenticateAsync(_configuration["SmtpSettings:Username"], _configuration["SmtpSettings:Password"]);
                await client.SendAsync(message);
                await client.DisconnectAsync(true);
            }

            return View("EmailSent");
        }

        // Titkosítási Logika
        private string EncryptResults(List<QuestionViewModel> answers, string userName, string email)
        {
            // Adatok sorosítása
            var data = new
            {
                UserName = userName,
                Email = email,
                Answers = answers,
                CompletedAt = DateTime.UtcNow
            };

            string jsonData = JsonSerializer.Serialize(data);

            // Adatok titkosítása
            using (Aes aes = Aes.Create())
            {
                aes.Key = GetEncryptionKey(); // Biztonságosan tárolt kulcs
                aes.GenerateIV();
                var iv = aes.IV;

                var encryptor = aes.CreateEncryptor(aes.Key, iv);

                using (var ms = new MemoryStream())
                {
                    // IV előtagolása
                    ms.Write(iv, 0, iv.Length);

                    using (var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
                    using (var sw = new StreamWriter(cs))
                    {
                        sw.Write(jsonData);
                    }

                    return Convert.ToBase64String(ms.ToArray());
                }
            }
        }

        // Biztonságosan tárolt titkosítási kulcs lekérése
        private byte[] GetEncryptionKey()
        {
            // Kulcs tárolása környezeti változóban vagy titkos tárolóban
            string keyString = Environment.GetEnvironmentVariable("QUIZ_ENCRYPTION_KEY");
            if (string.IsNullOrEmpty(keyString))
            {
                // Kulcs generálása, ha nem létezik (csak az első beállításkor)
                using (Aes aes = Aes.Create())
                {
                    aes.GenerateKey();
                    keyString = Convert.ToBase64String(aes.Key);
                    // Kulcs biztonságos tárolása a jövőbeni használathoz
                    // Példa: Mentés biztonságos konfigurációba vagy környezeti változóba
                }
            }
            return Convert.FromBase64String(keyString);
        }
    }
}

ViewModels Létrehozása

A ViewModel-ek a nézetekhez tartozó adatokat reprezentálják. Hozz létre egy új mappát ViewModels néven, és adj hozzá két osztályt: UserInfoViewModel.cs és QuestionViewModel.cs.

UserInfoViewModel.cs

using System.ComponentModel.DataAnnotations;

namespace TelecomQuizApp.ViewModels
{
    public class UserInfoViewModel
    {
        [Required]
        [Display(Name = "Név")]
        public string UserName { get; set; }

        [Required]
        [EmailAddress]
        [Display(Name = "Email cím")]
        public string Email { get; set; }
    }
}

QuestionViewModel.cs

using System.ComponentModel.DataAnnotations;

namespace TelecomQuizApp.ViewModels
{
    public class QuestionViewModel
    {
        public int QuestionId { get; set; }

        public string Content { get; set; }

        public string OptionA { get; set; }

        public string OptionB { get; set; }

        public string OptionC { get; set; }

        public string OptionD { get; set; }

        public int TimeAllocated { get; set; } // Másodpercekben

        public int CurrentQuestionNumber { get; set; }

        [Required]
        [Display(Name = "Válasz")]
        public string SelectedOption { get; set; }

        public TimeSpan TimeTaken { get; set; } // Az adott kérdésre fordított idő
    }
}

Nézetek Létrehozása

Hozz létre négy nézetet: Start.cshtml, Quiz.cshtml, Result.cshtml, és EmailSent.cshtml a Views/Quiz mappában.

Start.cshtml

Ez a nézet gyűjti össze a felhasználó nevét és email címét.

@model TelecomQuizApp.ViewModels.UserInfoViewModel

@{
    ViewData["Title"] = "Quiz Kezdése";
}

<h2>Quiz Kezdése</h2>

<form asp-action="Start" method="post">
    <div class="form-group">
        <label asp-for="UserName"></label>
        <input asp-for="UserName" class="form-control" />
        <span asp-validation-for="UserName" class="text-danger"></span>
    </div>
    <div class="form-group">
        <label asp-for="Email"></label>
        <input asp-for="Email" class="form-control" />
        <span asp-validation-for="Email" class="text-danger"></span>
    </div>
    <button type="submit" class="btn btn-primary">Quiz Indítása</button>
</form>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}
}

Quiz.cshtml

Ez a nézet jeleníti meg az aktuális kérdést és a válaszlehetőségeket, valamint kezeli az időzítőt.

@model TelecomQuizApp.ViewModels.QuestionViewModel

@{
    ViewData["Title"] = $"Kérdés {Model.CurrentQuestionNumber}";
}

<h2>Kérdés @Model.CurrentQuestionNumber</h2>

<form asp-action="Quiz" method="post">
    <div class="form-group">
        <p>@Model.Content</p>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="A" id="optionA" required />
            <label class="form-check-label" for="optionA">
                @Model.OptionA
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="B" id="optionB" required />
            <label class="form-check-label" for="optionB">
                @Model.OptionB
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="C" id="optionC" required />
            <label class="form-check-label" for="optionC">
                @Model.OptionC
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="D" id="optionD" required />
            <label class="form-check-label" for="optionD">
                @Model.OptionD
            </label>
        </div>
    </div>
    <input type="hidden" name="QuestionId" value="@Model.QuestionId" />
    <input type="hidden" name="CurrentQuestionNumber" value="@Model.CurrentQuestionNumber" />
    <input type="hidden" name="TimeTaken" id="TimeTaken" value="00:00:00" />
    <button type="submit" class="btn btn-primary">Következő</button>
</form>

@section Scripts {
    <script>
        // Időzítő logika
        var timeLeft = @Model.TimeAllocated; // Másodpercekben
        var timerElement = document.createElement("div");
        timerElement.innerHTML = "Hátralévő idő: <span id='timer'>" + timeLeft + "</span> másodperc";
        document.body.insertBefore(timerElement, document.body.firstChild);

        var startTime = Date.now();

        var timerInterval = setInterval(function () {
            timeLeft--;
            document.getElementById("timer").innerText = timeLeft;

            var elapsedTime = Math.floor((Date.now() - startTime) / 1000);
            var timeTaken = new Date(null);
            timeTaken.setSeconds(elapsedTime);
            var timeTakenStr = timeTaken.toISOString().substr(11, 8);
            document.getElementById("TimeTaken").value = timeTakenStr;

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                document.forms[0].submit();
            }
        }, 1000);
    </script>
}

Result.cshtml

Ez a nézet tájékoztatja a felhasználót a quiz befejezéséről, és lehetőséget ad az eredmények emailben történő küldésére.

@model TelecomQuizApp.Models.TestResult

@{
    ViewData["Title"] = "Quiz Eredmény";
}

<h2>Quiz Befejezve</h2>

<p>Köszönjük a részvételt, @Model.UserName!</p>
<p>A válaszaid titkosítva lettek mentve.</p>

<form asp-action="SendResult" method="post">
    <input type="hidden" name="TestResultId" value="@Model.Id" />
    <button type="submit" class="btn btn-primary">Eredmények E-mailben</button>
</form>

EmailSent.cshtml

Ez a nézet tájékoztatja a felhasználót, hogy az eredmények sikeresen elküldésre kerültek.

@{
    ViewData["Title"] = "Email Küldve";
}

<h2>Email Küldve</h2>

<p>A titkosított eredményeid el lettek küldve az email címedre.</p>

Eredmények Titkosítása és Email Küldése

Titkosítási Kulcs Beállítása

A titkosítási kulcsot biztonságosan kell tárolni, például környezeti változóként. Kövesd az alábbi lépéseket a kulcs generálásához és beállításához:
	1.	Kulcs Generálása:
Futtass egy egyszerű C# programot, hogy generálj egy AES kulcsot:

using System;
using System.Security.Cryptography;

class Program
{
    static void Main()
    {
        using (Aes aes = Aes.Create())
        {
            aes.GenerateKey();
            Console.WriteLine(Convert.ToBase64String(aes.Key));
        }
    }
}

Futtatás:
	•	Hozz létre egy új Console Application projektet, vagy használj egy online C# futtatót.
	•	Futtasd a programot, és másold ki a generált kulcsot.

	2.	Környezeti Változó Beállítása:
	•	Windows:
Nyisd meg a PowerShell-t és futtasd:

[System.Environment]::SetEnvironmentVariable("QUIZ_ENCRYPTION_KEY", "<YourBase64EncodedKey>", "User")


	•	Linux/macOS:
Nyisd meg a terminált és futtasd:

export QUIZ_ENCRYPTION_KEY=<YourBase64EncodedKey>


Megjegyzés: Biztosítsd, hogy a kulcs ne kerüljenek ki nyilvánosságra, és ne tárold a forráskódban.

Email Küldési Funkció Implementálása

A QuizController-ben már implementáltuk a SendResult akciót, amely e-mailben küldi el a titkosított eredményeket. Győződj meg róla, hogy az appsettings.json-ban megfelelően be vannak állítva az SMTP beállítások.

appsettings.json Beállítása

Adj hozzá SMTP beállításokat az appsettings.json fájlhoz:

{
  "ConnectionStrings": {
    "DefaultConnection": "server=localhost;database=testapi;user=quizuser;password=securepassword;SslMode=None;"
  },
  "SmtpSettings": {
    "Server": "smtp.your-email-provider.com",
    "Port": 587,
    "SenderName": "Quiz Rendszer",
    "SenderEmail": "no-reply@yourdomain.com",
    "Username": "your-email@example.com",
    "Password": "your-email-password"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}

Fontos:
	•	Cseréld ki a Server, Port, SenderName, SenderEmail, Username, és Password mezőket a saját email szolgáltatódnak megfelelő értékekre.
	•	Biztonsági Megjegyzés: Soha ne tárold az email jelszavakat a forráskódban. Használj környezeti változókat vagy titkos tárolókat (pl. Azure Key Vault) az éles környezetben.

SendResult Akció Frissítése

Győződj meg róla, hogy a SendResult akció a QuizController-ben a appsettings.json-ból olvassa be az SMTP beállításokat:

[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> SendResult(int TestResultId)
{
    var testResult = await _context.TestResults.FindAsync(TestResultId);
    if (testResult == null)
    {
        return NotFound();
    }

    // Email összeállítása
    var message = new MimeMessage();
    message.From.Add(new MailboxAddress(_configuration["SmtpSettings:SenderName"], _configuration["SmtpSettings:SenderEmail"]));
    message.To.Add(new MailboxAddress(testResult.UserName, testResult.Email));
    message.Subject = "A Quiz Eredményei";

    var body = new TextPart("plain")
    {
        Text = "Köszönjük a részvételt a quizben. Az eredményeidet titkosítva csatoltad."
    };

    // Titkosított adat csatolása szövegfájlként
    var attachment = new MimePart("text", "plain")
    {
        Content = new MimeContent(new MemoryStream(Encoding.UTF8.GetBytes(testResult.EncryptedData)), ContentEncoding.Default),
        ContentDisposition = new ContentDisposition(ContentDisposition.Attachment),
        ContentTransferEncoding = ContentEncoding.Base64,
        FileName = $"QuizResult_{testResult.Id}.txt"
    };

    var multipart = new Multipart("mixed");
    multipart.Add(body);
    multipart.Add(attachment);

    message.Body = multipart;

    // Email küldése
    using (var client = new SmtpClient())
    {
        // SSL tanúsítvány ellenőrzés kikapcsolása (nem javasolt éles környezetben)
        client.ServerCertificateValidationCallback = (s, c, h, e) => true;

        await client.ConnectAsync(_configuration["SmtpSettings:Server"], int.Parse(_configuration["SmtpSettings:Port"]), MailKit.Security.SecureSocketOptions.StartTls);
        await client.AuthenticateAsync(_configuration["SmtpSettings:Username"], _configuration["SmtpSettings:Password"]);
        await client.SendAsync(message);
        await client.DisconnectAsync(true);
    }

    return View("EmailSent");
}

Biztonsági Intézkedések

A biztonság kiemelten fontos, különösen, ha érzékeny adatokat kezelünk. Az alábbiakban néhány kulcsfontosságú biztonsági intézkedést mutatok be:
	1.	Titkosítási Kulcs Biztonságos Tárolása:
	•	Soha ne tárold a titkosítási kulcsot a forráskódban.
	•	Használj környezeti változókat vagy titkos tárolókat (pl. Azure Key Vault) a kulcsok biztonságos kezelésére.
	2.	HTTPS Használata:
	•	Győződj meg arról, hogy az alkalmazás HTTPS-en keresztül érhető el, hogy az adatátvitel titkosítva legyen.
	•	Beállíthatod az HTTPS átirányítást a Program.cs-ben:

app.UseHttpsRedirection();


	3.	Adatbázis Hitelesítés és Jogosultságok:
	•	Ne használd a root felhasználót az alkalmazás számára.
	•	Hozz létre egy dedikált felhasználót korlátozott jogosultságokkal az adatbázisban.
	4.	Input Validáció és Sanitizálás:
	•	Használj adatvalidációt a modellekben és a kontroller akciókban a potenciális SQL Injection és más támadások megelőzésére.
	5.	Session Kezelés:
	•	Állítsd be a session timeout értékét megfelelően.
	•	Használj biztonságos cookie-kat (HttpOnly, Secure).
	6.	Hibakezelés:
	•	Ne jeleníts meg részletes hibainformációkat a felhasználóknak.
	•	Használj egyéni hibaoldalakat és loggolj biztonságosan.
	7.	Rate Limiting és Túlterhelés Védelem:
	•	Implementálj rate limiting-et az email küldési funkcióhoz, hogy megakadályozd a visszaéléseket.
	8.	Email Hitelesítés:
	•	Használj erős hitelesítést az SMTP szerveren keresztül.
	•	Ne tárold az email jelszavakat a forráskódban.

Teljes Projekt Összefoglalása

Íme a teljes projekt áttekintése és a legfontosabb fájlok tartalma.

1. appsettings.json

{
  "ConnectionStrings": {
    "DefaultConnection": "server=localhost;database=testapi;user=quizuser;password=securepassword;SslMode=None;"
  },
  "SmtpSettings": {
    "Server": "smtp.your-email-provider.com",
    "Port": 587,
    "SenderName": "Quiz Rendszer",
    "SenderEmail": "no-reply@yourdomain.com",
    "Username": "your-email@example.com",
    "Password": "your-email-password"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}

Megjegyzés: Cseréld ki a DefaultConnection és SmtpSettings értékeket a saját környezetednek megfelelően.

2. Program.cs

using Microsoft.EntityFrameworkCore;
using TelecomQuizApp.Data;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Entity Framework konfigurálása MySQL-lel
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));

// Session konfigurálása
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// Swagger szolgáltatások hozzáadása
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "TelecomQuiz API",
        Version = "v1",
        Description = "API dokumentáció a TelecomQuiz alkalmazáshoz"
    });

    // Opció: XML dokumentáció engedélyezése (ha van)
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        c.IncludeXmlComments(xmlPath);
    }
});

var app = builder.Build();

// HTTP request pipeline konfigurálása
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// Swagger middleware hozzáadása (fejlesztési környezetben)
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "TelecomQuiz API V1");
        c.RoutePrefix = "swagger"; // Elérhetőség: https://localhost:<port>/swagger
    });
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

// Session használata
app.UseSession();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Quiz}/{action=Start}/{id?}");

app.Run();

3. Models/ApplicationDbContext.cs

Az Entity Framework Core által generált ApplicationDbContext.cs tartalmazza a táblákhoz tartozó DbSet-eket.

using Microsoft.EntityFrameworkCore;

namespace TelecomQuizApp.Data
{
    public partial class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext()
        {
        }

        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Question> Questions { get; set; }
        public virtual DbSet<UserResponse> UserResponses { get; set; }
        public virtual DbSet<TestResult> TestResults { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Question>(entity =>
            {
                entity.ToTable("Questions");

                entity.HasKey(e => e.Id);

                entity.Property(e => e.Content)
                    .IsRequired()
                    .HasMaxLength(65535);

                entity.Property(e => e.OptionA)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.OptionB)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.OptionC)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.OptionD)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.CorrectOption)
                    .IsRequired()
                    .HasMaxLength(1);
            });

            modelBuilder.Entity<UserResponse>(entity =>
            {
                entity.ToTable("UserResponses");

                entity.HasKey(e => e.Id);

                entity.Property(e => e.UserName)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.Email)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.SelectedOption)
                    .IsRequired()
                    .HasMaxLength(1);

                entity.HasOne(d => d.Question)
                    .WithMany(p => p.UserResponses)
                    .HasForeignKey(d => d.QuestionId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("FK_UserResponses_Questions");
            });

            modelBuilder.Entity<TestResult>(entity =>
            {
                entity.ToTable("TestResults");

                entity.HasKey(e => e.Id);

                entity.Property(e => e.UserName)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.Email)
                    .IsRequired()
                    .HasMaxLength(255);

                entity.Property(e => e.EncryptedData)
                    .IsRequired()
                    .HasMaxLength(65535);
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}

4. Modellek (Automatikusan Generálva)

Az Entity Framework Core generálta a modelleket a Scaffold-DbContext parancs alapján. Győződj meg róla, hogy a Models mappában megtalálhatók-e a következő osztályok:
	•	Question.cs
	•	UserResponse.cs
	•	TestResult.cs

Ezek a modellek már megfelelnek az adatbázis tábláinak.

QuizController és Nézetek Létrehozása

QuizController.cs

A QuizController kezeli a quiz folyamatát: kezdés, kérdések megjelenítése, válaszok rögzítése, eredmények tárolása és email küldése.

using Microsoft.AspNetCore.Mvc;
using TelecomQuizApp.Data;
using TelecomQuizApp.Models;
using TelecomQuizApp.ViewModels;
using System.Threading.Tasks;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using MimeKit;
using MailKit.Net.Smtp;

namespace TelecomQuizApp.Controllers
{
    public class QuizController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly IConfiguration _configuration;

        public QuizController(ApplicationDbContext context, IConfiguration configuration)
        {
            _context = context;
            _configuration = configuration;
        }

        // GET: Quiz/Start
        public IActionResult Start()
        {
            return View();
        }

        // POST: Quiz/Start
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Start(UserInfoViewModel model)
        {
            if (ModelState.IsValid)
            {
                // Felhasználói információk tárolása session-ben
                HttpContext.Session.SetString("UserName", model.UserName);
                HttpContext.Session.SetString("Email", model.Email);
                // Inicializáljuk az answeredQuestions listát
                HttpContext.Session.SetString("AnsweredQuestions", JsonSerializer.Serialize(new List<QuestionViewModel>()));
                return RedirectToAction("Quiz");
            }
            return View(model);
        }

        // GET: Quiz/Quiz
        public async Task<IActionResult> Quiz()
        {
            // Ellenőrizzük, hogy a felhasználói adatok elérhetőek-e
            var userName = HttpContext.Session.GetString("UserName");
            var email = HttpContext.Session.GetString("Email");

            if (string.IsNullOrEmpty(userName) || string.IsNullOrEmpty(email))
            {
                return RedirectToAction("Start");
            }

            // Lekérjük a már válaszolt kérdéseket
            var answeredQuestionsJson = HttpContext.Session.GetString("AnsweredQuestions");
            var answeredQuestions = JsonSerializer.Deserialize<List<QuestionViewModel>>(answeredQuestionsJson);

            if (answeredQuestions.Count >= 10)
            {
                // Quiz befejezve
                return RedirectToAction("Result");
            }

            // Véletlenszerűen kiválasztunk egy kérdést, amit még nem válaszoltak meg
            var unansweredQuestions = _context.Questions.Where(q => !answeredQuestions.Any(aq => aq.QuestionId == q.Id)).ToList();

            if (!unansweredQuestions.Any())
            {
                // Nincs több kérdés, de a kérdések száma nem éri el a 10-et
                // Itt kezelhetjük, például új kérdéseket adhatsz hozzá
                return RedirectToAction("Result");
            }

            var random = new Random();
            var question = unansweredQuestions[random.Next(unansweredQuestions.Count)];

            // Idő kalkulálása a komplexitás alapján (pl. 30 másodperc per komplexitási szint)
            int timeAllocated = question.Complexity * 30;

            var viewModel = new QuestionViewModel
            {
                QuestionId = question.Id,
                Content = question.Content,
                OptionA = question.OptionA,
                OptionB = question.OptionB,
                OptionC = question.OptionC,
                OptionD = question.OptionD,
                TimeAllocated = timeAllocated,
                CurrentQuestionNumber = answeredQuestions.Count + 1
            };

            return View(viewModel);
        }

        // POST: Quiz/Quiz
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Quiz(QuestionViewModel model)
        {
            if (ModelState.IsValid)
            {
                // Lekérjük a már válaszolt kérdéseket
                var answeredQuestionsJson = HttpContext.Session.GetString("AnsweredQuestions");
                var answeredQuestions = JsonSerializer.Deserialize<List<QuestionViewModel>>(answeredQuestionsJson);

                // Rögzítjük az aktuális választ
                answeredQuestions.Add(new QuestionViewModel
                {
                    QuestionId = model.QuestionId,
                    SelectedOption = model.SelectedOption,
                    TimeTaken = model.TimeTaken,
                    CurrentQuestionNumber = model.CurrentQuestionNumber
                });

                // Frissítjük a session-t
                HttpContext.Session.SetString("AnsweredQuestions", JsonSerializer.Serialize(answeredQuestions));

                if (answeredQuestions.Count >= 10)
                {
                    // Quiz befejezve
                    return RedirectToAction("Result");
                }

                return RedirectToAction("Quiz");
            }

            return View(model);
        }

        // GET: Quiz/Result
        public async Task<IActionResult> Result()
        {
            var userName = HttpContext.Session.GetString("UserName");
            var email = HttpContext.Session.GetString("Email");
            var answeredQuestionsJson = HttpContext.Session.GetString("AnsweredQuestions");
            var answeredQuestions = JsonSerializer.Deserialize<List<QuestionViewModel>>(answeredQuestionsJson);

            if (string.IsNullOrEmpty(userName) || string.IsNullOrEmpty(email) || answeredQuestions == null)
            {
                return RedirectToAction("Start");
            }

            // Generáljuk az eredmény adatokat és titkosítjuk
            var encryptedData = EncryptResults(answeredQuestions, userName, email);

            // Mentjük az eredményt az adatbázisba
            var testResult = new TestResult
            {
                UserName = userName,
                Email = email,
                CompletedAt = DateTime.UtcNow,
                EncryptedData = encryptedData
            };

            _context.TestResults.Add(testResult);
            await _context.SaveChangesAsync();

            // Töröljük a session adatokat
            HttpContext.Session.Clear();

            return View(testResult);
        }

        // POST: Quiz/SendResult
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> SendResult(int TestResultId)
        {
            var testResult = await _context.TestResults.FindAsync(TestResultId);
            if (testResult == null)
            {
                return NotFound();
            }

            // Email összeállítása
            var message = new MimeMessage();
            message.From.Add(new MailboxAddress(_configuration["SmtpSettings:SenderName"], _configuration["SmtpSettings:SenderEmail"]));
            message.To.Add(new MailboxAddress(testResult.UserName, testResult.Email));
            message.Subject = "A Quiz Eredményei";

            var body = new TextPart("plain")
            {
                Text = "Köszönjük a részvételt a quizben. Az eredményeidet titkosítva csatoltad."
            };

            // Titkosított adat csatolása szövegfájlként
            var attachment = new MimePart("text", "plain")
            {
                Content = new MimeContent(new MemoryStream(Encoding.UTF8.GetBytes(testResult.EncryptedData)), ContentEncoding.Default),
                ContentDisposition = new ContentDisposition(ContentDisposition.Attachment),
                ContentTransferEncoding = ContentEncoding.Base64,
                FileName = $"QuizResult_{testResult.Id}.txt"
            };

            var multipart = new Multipart("mixed");
            multipart.Add(body);
            multipart.Add(attachment);

            message.Body = multipart;

            // Email küldése
            using (var client = new SmtpClient())
            {
                // SSL tanúsítvány ellenőrzés kikapcsolása (nem javasolt éles környezetben)
                client.ServerCertificateValidationCallback = (s, c, h, e) => true;

                await client.ConnectAsync(_configuration["SmtpSettings:Server"], int.Parse(_configuration["SmtpSettings:Port"]), MailKit.Security.SecureSocketOptions.StartTls);
                await client.AuthenticateAsync(_configuration["SmtpSettings:Username"], _configuration["SmtpSettings:Password"]);
                await client.SendAsync(message);
                await client.DisconnectAsync(true);
            }

            return View("EmailSent");
        }

        // Titkosítási Logika
        private string EncryptResults(List<QuestionViewModel> answers, string userName, string email)
        {
            // Adatok sorosítása
            var data = new
            {
                UserName = userName,
                Email = email,
                Answers = answers,
                CompletedAt = DateTime.UtcNow
            };

            string jsonData = JsonSerializer.Serialize(data);

            // Adatok titkosítása
            using (Aes aes = Aes.Create())
            {
                aes.Key = GetEncryptionKey(); // Biztonságosan tárolt kulcs
                aes.GenerateIV();
                var iv = aes.IV;

                var encryptor = aes.CreateEncryptor(aes.Key, iv);

                using (var ms = new MemoryStream())
                {
                    // IV előtagolása
                    ms.Write(iv, 0, iv.Length);

                    using (var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
                    using (var sw = new StreamWriter(cs))
                    {
                        sw.Write(jsonData);
                    }

                    return Convert.ToBase64String(ms.ToArray());
                }
            }
        }

        // Biztonságosan tárolt titkosítási kulcs lekérése
        private byte[] GetEncryptionKey()
        {
            // Kulcs tárolása környezeti változóban vagy titkos tárolóban
            string keyString = Environment.GetEnvironmentVariable("QUIZ_ENCRYPTION_KEY");
            if (string.IsNullOrEmpty(keyString))
            {
                // Kulcs generálása, ha nem létezik (csak az első beállításkor)
                using (Aes aes = Aes.Create())
                {
                    aes.GenerateKey();
                    keyString = Convert.ToBase64String(aes.Key);
                    // Kulcs biztonságos tárolása a jövőbeni használathoz
                    // Példa: Mentés biztonságos konfigurációba vagy környezeti változóba
                }
            }
            return Convert.FromBase64String(keyString);
        }
    }
}

Nézetek Létrehozása

Start.cshtml

Ez a nézet gyűjti össze a felhasználó nevét és email címét.

@model TelecomQuizApp.ViewModels.UserInfoViewModel

@{
    ViewData["Title"] = "Quiz Kezdése";
}

<h2>Quiz Kezdése</h2>

<form asp-action="Start" method="post">
    <div class="form-group">
        <label asp-for="UserName"></label>
        <input asp-for="UserName" class="form-control" />
        <span asp-validation-for="UserName" class="text-danger"></span>
    </div>
    <div class="form-group">
        <label asp-for="Email"></label>
        <input asp-for="Email" class="form-control" />
        <span asp-validation-for="Email" class="text-danger"></span>
    </div>
    <button type="submit" class="btn btn-primary">Quiz Indítása</button>
</form>

@section Scripts {
    @{await Html.RenderPartialAsync("_ValidationScriptsPartial");}
}

Quiz.cshtml

Ez a nézet jeleníti meg az aktuális kérdést és a válaszlehetőségeket, valamint kezeli az időzítőt.

@model TelecomQuizApp.ViewModels.QuestionViewModel

@{
    ViewData["Title"] = $"Kérdés {Model.CurrentQuestionNumber}";
}

<h2>Kérdés @Model.CurrentQuestionNumber</h2>

<form asp-action="Quiz" method="post">
    <div class="form-group">
        <p>@Model.Content</p>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="A" id="optionA" required />
            <label class="form-check-label" for="optionA">
                @Model.OptionA
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="B" id="optionB" required />
            <label class="form-check-label" for="optionB">
                @Model.OptionB
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="C" id="optionC" required />
            <label class="form-check-label" for="optionC">
                @Model.OptionC
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" asp-for="SelectedOption" value="D" id="optionD" required />
            <label class="form-check-label" for="optionD">
                @Model.OptionD
            </label>
        </div>
    </div>
    <input type="hidden" name="QuestionId" value="@Model.QuestionId" />
    <input type="hidden" name="CurrentQuestionNumber" value="@Model.CurrentQuestionNumber" />
    <input type="hidden" name="TimeTaken" id="TimeTaken" value="00:00:00" />
    <button type="submit" class="btn btn-primary">Következő</button>
</form>

@section Scripts {
    <script>
        // Időzítő logika
        var timeLeft = @Model.TimeAllocated; // Másodpercekben
        var timerElement = document.createElement("div");
        timerElement.innerHTML = "Hátralévő idő: <span id='timer'>" + timeLeft + "</span> másodperc";
        document.body.insertBefore(timerElement, document.body.firstChild);

        var startTime = Date.now();

        var timerInterval = setInterval(function () {
            timeLeft--;
            document.getElementById("timer").innerText = timeLeft;

            var elapsedTime = Math.floor((Date.now() - startTime) / 1000);
            var timeTaken = new Date(null);
            timeTaken.setSeconds(elapsedTime);
            var timeTakenStr = timeTaken.toISOString().substr(11, 8);
            document.getElementById("TimeTaken").value = timeTakenStr;

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                document.forms[0].submit();
            }
        }, 1000);
    </script>
}

Result.cshtml

Ez a nézet tájékoztatja a felhasználót a quiz befejezéséről, és lehetőséget ad az eredmények emailben történő küldésére.

@model TelecomQuizApp.Models.TestResult

@{
    ViewData["Title"] = "Quiz Eredmény";
}

<h2>Quiz Befejezve</h2>

<p>Köszönjük a részvételt, @Model.UserName!</p>
<p>A válaszaid titkosítva lettek mentve.</p>

<form asp-action="SendResult" method="post">
    <input type="hidden" name="TestResultId" value="@Model.Id" />
    <button type="submit" class="btn btn-primary">Eredmények E-mailben</button>
</form>

EmailSent.cshtml

Ez a nézet tájékoztatja a felhasználót, hogy az eredmények sikeresen elküldésre kerültek.

@{
    ViewData["Title"] = "Email Küldve";
}

<h2>Email Küldve</h2>

<p>A titkosított eredményeid el lettek küldve az email címedre.</p>

Eredmények Titkosítása és Email Küldése

Titkosítási Kulcs Beállítása

A titkosítási kulcsot biztonságosan kell tárolni, például környezeti változóként. Kövesd az alábbi lépéseket a kulcs generálásához és beállításához:
	1.	Kulcs Generálása:
Futtass egy egyszerű C# programot, hogy generálj egy AES kulcsot:

using System;
using System.Security.Cryptography;

class Program
{
    static void Main()
    {
        using (Aes aes = Aes.Create())
        {
            aes.GenerateKey();
            Console.WriteLine(Convert.ToBase64String(aes.Key));
        }
    }
}

Futtatás:
	•	Hozz létre egy új Console Application projektet, vagy használj egy online C# futtatót.
	•	Futtasd a programot, és másold ki a generált kulcsot.

	2.	Környezeti Változó Beállítása:
	•	Windows:
Nyisd meg a PowerShell-t és futtasd:

[System.Environment]::SetEnvironmentVariable("QUIZ_ENCRYPTION_KEY", "<YourBase64EncodedKey>", "User")


	•	Linux/macOS:
Nyisd meg a terminált és futtasd:

export QUIZ_ENCRYPTION_KEY=<YourBase64EncodedKey>


Megjegyzés: Biztosítsd, hogy a kulcs ne kerüljenek ki nyilvánosságra, és ne tárold a forráskódban.

Email Küldési Funkció Implementálása

A QuizController-ben már implementáltuk a SendResult akciót, amely e-mailben küldi el a titkosított eredményeket. Győződj meg róla, hogy az appsettings.json-ban megfelelően be vannak állítva az SMTP beállítások.

appsettings.json Beállítása

Adj hozzá SMTP beállításokat az appsettings.json fájlhoz:

{
  "ConnectionStrings": {
    "DefaultConnection": "server=localhost;database=testapi;user=quizuser;password=securepassword;SslMode=None;"
  },
  "SmtpSettings": {
    "Server": "smtp.your-email-provider.com",
    "Port": 587,
    "SenderName": "Quiz Rendszer",
    "SenderEmail": "no-reply@yourdomain.com",
    "Username": "your-email@example.com",
    "Password": "your-email-password"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}

Fontos:
	•	Cseréld ki a Server, Port, SenderName, SenderEmail, Username, és Password mezőket a saját email szolgáltatódnak megfelelő értékekre.
	•	Biztonsági Megjegyzés: Soha ne tárold az email jelszavakat a forráskódban. Használj környezeti változókat vagy titkos tárolókat (pl. Azure Key Vault) az éles környezetben.

SendResult Akció Frissítése

Győződj meg róla, hogy a SendResult akció a QuizController-ben a appsettings.json-ból olvassa be az SMTP beállításokat:

[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> SendResult(int TestResultId)
{
    var testResult = await _context.TestResults.FindAsync(TestResultId);
    if (testResult == null)
    {
        return NotFound();
    }

    // Email összeállítása
    var message = new MimeMessage();
    message.From.Add(new MailboxAddress(_configuration["SmtpSettings:SenderName"], _configuration["SmtpSettings:SenderEmail"]));
    message.To.Add(new MailboxAddress(testResult.UserName, testResult.Email));
    message.Subject = "A Quiz Eredményei";

    var body = new TextPart("plain")
    {
        Text = "Köszönjük a részvételt a quizben. Az eredményeidet titkosítva csatoltad."
    };

    // Titkosított adat csatolása szövegfájlként
    var attachment = new MimePart("text", "plain")
    {
        Content = new MimeContent(new MemoryStream(Encoding.UTF8.GetBytes(testResult.EncryptedData)), ContentEncoding.Default),
        ContentDisposition = new ContentDisposition(ContentDisposition.Attachment),
        ContentTransferEncoding = ContentEncoding.Base64,
        FileName = $"QuizResult_{testResult.Id}.txt"
    };

    var multipart = new Multipart("mixed");
    multipart.Add(body);
    multipart.Add(attachment);

    message.Body = multipart;

    // Email küldése
    using (var client = new SmtpClient())
    {
        // SSL tanúsítvány ellenőrzés kikapcsolása (nem javasolt éles környezetben)
        client.ServerCertificateValidationCallback = (s, c, h, e) => true;

        await client.ConnectAsync(_configuration["SmtpSettings:Server"], int.Parse(_configuration["SmtpSettings:Port"]), MailKit.Security.SecureSocketOptions.StartTls);
        await client.AuthenticateAsync(_configuration["SmtpSettings:Username"], _configuration["SmtpSettings:Password"]);
        await client.SendAsync(message);
        await client.DisconnectAsync(true);
    }

    return View("EmailSent");
}

Biztonsági Intézkedések

Ahhoz, hogy az alkalmazás biztonságos maradjon és a felhasználók ne tudják megkerülni a védelmi mechanizmusokat, az alábbi biztonsági intézkedéseket kell betartani:
	1.	Titkosítási Kulcs Biztonságos Tárolása:
	•	Soha ne tárold a titkosítási kulcsot a forráskódban.
	•	Használj környezeti változókat vagy titkos tárolókat (pl. Azure Key Vault) a kulcsok biztonságos kezelésére.
	2.	HTTPS Használata:
	•	Győződj meg arról, hogy az alkalmazás HTTPS-en keresztül érhető el, hogy az adatátvitel titkosítva legyen.
	•	Beállíthatod az HTTPS átirányítást a Program.cs-ben:

app.UseHttpsRedirection();


	3.	Adatbázis Hitelesítés és Jogosultságok:
	•	Ne használd a root felhasználót az alkalmazás számára.
	•	Hozz létre egy dedikált felhasználót korlátozott jogosultságokkal az adatbázisban.
	4.	Input Validáció és Sanitizálás:
	•	Használj adatvalidációt a modellekben és a kontroller akciókban a potenciális SQL Injection és más támadások megelőzésére.
	•	Az MVC modellek [Required], [EmailAddress], stb. attribútumokkal segítik az input validációt.
	5.	Session Kezelés:
	•	Állítsd be a session timeout értékét megfelelően.
	•	Használj biztonságos cookie-kat (HttpOnly, Secure).
	6.	Hibakezelés:
	•	Ne jeleníts meg részletes hibainformációkat a felhasználóknak.
	•	Használj egyéni hibaoldalakat és loggolj biztonságosan.
	7.	Rate Limiting és Túlterhelés Védelem:
	•	Implementálj rate limiting-et az email küldési funkcióhoz, hogy megakadályozd a visszaéléseket.
	•	Ehhez használhatsz middleware-eket vagy külső szolgáltatásokat, például AspNetCoreRateLimit csomagot.
	8.	Email Hitelesítés:
	•	Használj erős hitelesítést az SMTP szerveren keresztül.
	•	Ne tárold az email jelszavakat a forráskódban.
	9.	Swagger Biztonságos Használata:
	•	Korlátozd a Swagger UI elérését fejlesztési környezetben.
	•	Éles környezetben ne engedélyezd a Swagger UI-t, mivel érzékeny információkat jeleníthet meg.
	10.	Csak Szükséges Végpontok Dokumentálása:
	•	Csak azokat az API végpontokat dokumentáld a Swagger-rel, amelyekre szükség van, és amelyek biztonságosak a publikus eléréshez.
	•	Kerüld a belső vagy adminisztrációs végpontok dokumentálását.

Teljes Projekt Összefoglalása

A következőkben bemutatom a teljes projekt szerkezetét és a legfontosabb fájlok tartalmát.

1. appsettings.json

{
  "ConnectionStrings": {
    "DefaultConnection": "server=localhost;database=testapi;user=quizuser;password=securepassword;SslMode=None;"
  },
  "SmtpSettings": {
    "Server": "smtp.your-email-provider.com",
    "Port": 587,
    "SenderName": "Quiz Rendszer",
    "SenderEmail": "no-reply@yourdomain.com",
    "Username": "your-email@example.com",
    "Password": "your-email-password"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}

Megjegyzés: Cseréld ki a DefaultConnection és SmtpSettings értékeket a saját környezetednek megfelelően.

2. Program.cs

using Microsoft.EntityFrameworkCore;
using TelecomQuizApp.Data;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

// Entity Framework konfigurálása MySQL-lel
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString)));

// Session konfigurálása
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// Swagger szolgáltatások hozzáadása
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "TelecomQuiz API",
        Version = "v1",
        Description = "API dokumentáció a TelecomQuiz alkalmazáshoz"
    });

    // Opció: XML dokumentáció engedélyezése (ha van)
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        c.IncludeXmlComments(xmlPath);
    }
});

var app = builder.Build();

// HTTP request pipeline konfigurálása
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// Swagger middleware hozzáadása (fejlesztési környezetben)
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "TelecomQuiz API V1");
        c.RoutePrefix = "swagger"; // Elérhetőség: https://localhost:<port>/swagger
    });
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

// Session használata
app.UseSession();

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Quiz}/{action=Start}/{id?}");

app.Run();

3. Models/ApplicationDbContext.cs

A Models mappában található ApplicationDbContext.cs már tartalmazza a szükséges DbSet-eket, amelyeket az Entity Framework Core automatikusan generált.

4. ViewModels/UserInfoViewModel.cs

using System.ComponentModel.DataAnnotations;

namespace TelecomQuizApp.ViewModels
{
    public class UserInfoViewModel
    {
        [Required]
        [Display(Name = "Név")]
        public string UserName { get; set; }

        [Required]
        [EmailAddress]
        [Display(Name = "Email cím")]
        public string Email { get; set; }
    }
}

5. ViewModels/QuestionViewModel.cs

using System.ComponentModel.DataAnnotations;

namespace TelecomQuizApp.ViewModels
{
    public class QuestionViewModel
    {
        public int QuestionId { get; set; }

        public string Content { get; set; }

        public string OptionA { get; set; }

        public string OptionB { get; set; }

        public string OptionC { get; set; }

        public string OptionD { get; set; }

        public int TimeAllocated { get; set; } // Másodpercekben

        public int CurrentQuestionNumber { get; set; }

        [Required]
        [Display(Name = "Válasz")]
        public string SelectedOption { get; set; }

        public TimeSpan TimeTaken { get; set; } // Az adott kérdésre fordított idő
    }
}

6. Controllers/QuizController.cs

A QuizController már részletesen implementálva van az előzőekben.

7. Nézetek Létrehozása

Hozd létre a Views/Quiz mappában a Start.cshtml, Quiz.cshtml, Result.cshtml, és EmailSent.cshtml fájlokat a fentiek szerint.

8. Views/Shared/_Layout.cshtml és Views/Shared/_ValidationScriptsPartial.cshtml

Győződj meg róla, hogy a projektedben megfelelően be vannak állítva az elrendezések és a validációs script-ek.

_Layout.cshtml

Ez a fájl az alkalmazás fő elrendezését határozza meg. Győződj meg róla, hogy tartalmazza a Bootstrap CSS-t és JavaScript-et a stílus és funkcionalitás érdekében.

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>@ViewData["Title"] - TelecomQuizApp</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" />
    <link rel="stylesheet" href="~/css/site.css" />
</head>
<body>
    <div class="container">
        @RenderBody()
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
    @RenderSection("Scripts", required: false)
</body>
</html>

_ValidationScriptsPartial.cshtml

Ez a fájl tartalmazza a szükséges validációs script-eket.

<environment include="Development">
    <script src="~/lib/jquery-validation/dist/jquery.validate.js"></script>
    <script src="~/lib/jquery-validation-unobtrusive/jquery.validate.unobtrusive.js"></script>
</environment>
<environment exclude="Development">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.2/jquery.validate.min.js"
            integrity="sha256-FOsZ4u2HlYhgiP11sHWlYJ+ZPJymjzYgkHGm4dIBUKw="
            crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validation-unobtrusive/3.2.11/jquery.validate.unobtrusive.min.js"
            integrity="sha256-5cTf1oj7PppzWtDixVcgFsq0lPb4EcP3TprFgB02SvY="
            crossorigin="anonymous"></script>
</environment>

Záró Gondolatok

Ezzel a lépésről lépésre történő útmutatóval sikeresen létrehoztuk a kívánt távközlési technikus tanulók számára készült quiz alkalmazást. Az alkalmazás biztonságosan kezeli a felhasználói adatokat és eredményeket, valamint az eredményeket titkosítva küldi el emailben.

Kiemelt Pontok:
	•	Adatbázis Biztonság: A felhasználói adatok és eredmények biztonságosan kerülnek tárolásra, és az eredmények titkosítva kerülnek mentésre.
	•	Swagger Integráció: Az API dokumentáció automatikusan generálva van, ami megkönnyíti az API tesztelését és megértését.
	•	Session Kezelés: Az alkalmazás session-öket használ a felhasználói adatok és válaszok tárolására.
	•	Email Küldés: Az eredmények biztonságosan elküldhetők emailben, titkosított formában.

Javaslatok a Projekt Fejlesztéséhez:
	1.	Felhasználói Felület Finomhangolása:
	•	Használj modern CSS keretrendszereket (pl. Bootstrap) a reszponzív és felhasználóbarát felület kialakításához.
	•	Tedd interaktívvá a kérdések megjelenítését, például animációkkal vagy progress bar-ral.
	2.	Tesztelés:
	•	Alaposan teszteld az alkalmazást különböző scenáriókban, hogy megbizonyosodj arról, hogy minden funkció megfelelően működik.
	•	Használj unit és integrációs teszteket a stabilitás és megbízhatóság biztosítására.
	3.	Kiterjesztések és Funkcionalitások:
	•	Implementálj többkérdéses teszteket, ahol a kérdések egyszerre jelennek meg.
	•	Adj hozzá statisztikákat az eredményekhez, például pontszámokat, helyes válaszok arányát stb.
	•	Hozz létre adminisztrációs felületet a kérdések kezeléséhez (CRUD műveletek).
	4.	Biztonsági Audit:
	•	Rendszeresen végezz biztonsági auditokat az alkalmazáson, hogy az esetleges sebezhetőségeket időben felismerd és orvosold.
	•	Implementálj további biztonsági mechanizmusokat, például CSRF védelem, rate limiting, stb.
	5.	Felhőbe Áthelyezés:
	•	Fontold meg az alkalmazás és az adatbázis felhőbe történő áthelyezését (pl. Azure, AWS), hogy könnyebben skálázható és elérhető legyen.
	6.	Dokumentáció és Képzés:
	•	Készíts részletes dokumentációt az alkalmazás használatáról és karbantartásáról.
	•	Biztosíts képzést az adminisztrátorok és felhasználók számára az alkalmazás hatékony használatához.

Ha bármilyen további kérdésed van, vagy további részletekre van szükséged egy adott lépésben, nyugodtan jelezd!
